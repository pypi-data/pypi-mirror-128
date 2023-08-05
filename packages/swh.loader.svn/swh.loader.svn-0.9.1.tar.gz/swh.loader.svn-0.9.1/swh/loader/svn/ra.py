# Copyright (C) 2016-2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""Remote Access client to svn server.

"""

import codecs
import dataclasses
import os
import shutil
import tempfile
from typing import Dict, List, Optional, Tuple

import click
from subvertpy import delta, properties
from subvertpy.ra import Auth, RemoteAccess, get_username_provider

from swh.model import from_disk, hashutil
from swh.model.model import Content, Directory, SkippedContent

_eol_style = {"native": b"\n", "CRLF": b"\r\n", "LF": b"\n", "CR": b"\r"}


def _normalize_line_endings(lines, eol_style="native"):
    r"""Normalize line endings to unix (\\n), windows (\\r\\n) or mac (\\r).

    Args:
        lines (bytes): The lines to normalize

        line_ending (str): The line ending format as defined for
            svn:eol-style property. Acceptable values are 'native',
            'CRLF', 'LF' and 'CR'

    Returns:
        bytes: lines with endings normalized
    """
    if eol_style in _eol_style:
        lines = lines.replace(_eol_style["CRLF"], _eol_style["LF"]).replace(
            _eol_style["CR"], _eol_style["LF"]
        )
        if _eol_style[eol_style] != _eol_style["LF"]:
            lines = lines.replace(_eol_style["LF"], _eol_style[eol_style])

    return lines


def apply_txdelta_handler(sbuf, target_stream):
    """Return a function that can be called repeatedly with txdelta windows.
    When done, closes the target_stream.

    Adapted from subvertpy.delta.apply_txdelta_handler to close the
    stream when done.

    Args:
        sbuf: Source buffer
        target_stream: Target stream to write to.

    Returns:
        Function to be called to apply txdelta windows

    """

    def apply_window(window, sbuf=sbuf, target_stream=target_stream):
        if window is None:
            target_stream.close()
            return  # Last call
        patch = delta.apply_txdelta_window(sbuf, window)
        target_stream.write(patch)

    return apply_window


def read_svn_link(data):
    """Read the svn link's content.

    Args:
        data (bytes): svn link's raw content

    Returns:
        The tuple of (filetype, destination path)

    """
    split_byte = b" "
    filetype, *src = data.split(split_byte)
    src = split_byte.join(src)
    return filetype, src


def is_file_an_svnlink_p(fullpath):
    """Determine if a filepath is an svnlink or something else.

    Args:
        fullpath (str/bytes): Full path to the potential symlink to check

    Returns:
        boolean value to determine if it's indeed a symlink (as per
        svn) or not.

    """
    with open(fullpath, "rb") as f:
        filetype, src = read_svn_link(f.read())
        return filetype == b"link", src


def _ra_codecs_error_handler(e):
    """Subvertpy may fail to decode to utf-8 the user svn properties.  As
       they are not used by the loader, return an empty string instead
       of the decoded content.

    Args:
        e (UnicodeDecodeError): exception raised during the svn
                                properties decoding.

    """
    return "", e.end


DEFAULT_FLAG = 0
EXEC_FLAG = 1
NOEXEC_FLAG = 2

SVN_PROPERTY_EOL = "svn:eol-style"


@dataclasses.dataclass
class FileState:
    """Persists some file states (eg. end of lines style) across revisions while
    replaying them."""

    eol_style: Optional[str] = None
    """EOL state check mess"""

    svn_special_path_non_link_data: Optional[bytes] = None
    """keep track of non link file content with svn:special property set"""


class FileEditor:
    """File Editor in charge of updating file on disk and memory objects.

    """

    __slots__ = [
        "directory",
        "path",
        "fullpath",
        "executable",
        "link",
        "state",
    ]

    def __init__(self, directory, rootpath, path, state: FileState):
        self.directory = directory
        self.path = path
        # default value: 0, 1: set the flag, 2: remove the exec flag
        self.executable = DEFAULT_FLAG
        self.link = None
        self.fullpath = os.path.join(rootpath, path)
        self.state = state

    def change_prop(self, key, value):
        if key == properties.PROP_EXECUTABLE:
            if value is None:  # bit flip off
                self.executable = NOEXEC_FLAG
            else:
                self.executable = EXEC_FLAG
        elif key == properties.PROP_SPECIAL:
            # Possibly a symbolic link. We cannot check further at
            # that moment though, patch(s) not being applied yet
            self.link = value is not None
        elif key == SVN_PROPERTY_EOL:
            # backup end of line style for file
            self.state.eol_style = value

    def __make_symlink(self, src):
        """Convert the svnlink to a symlink on disk.

        This function expects self.fullpath to be a svn link.

        Args:
            src (bytes): Path to the link's source

        Return:
            tuple: The svnlink's data tuple:

                - type (should be only 'link')
                - <path-to-src>

        """
        os.remove(self.fullpath)
        os.symlink(src=src, dst=self.fullpath)

    def __make_svnlink(self):
        """Convert the symlink to a svnlink on disk.

        Return:
            The symlink's svnlink data (``b'type <path-to-src>'``)

        """
        # we replace the symlink by a svnlink
        # to be able to patch the file on future commits
        src = os.readlink(self.fullpath)
        os.remove(self.fullpath)
        sbuf = b"link " + src
        with open(self.fullpath, "wb") as f:
            f.write(sbuf)
        return sbuf

    def apply_textdelta(self, base_checksum):
        if os.path.lexists(self.fullpath):
            if os.path.islink(self.fullpath):
                # svn does not deal with symlink so we transform into
                # real svn symlink for potential patching in later
                # commits
                sbuf = self.__make_svnlink()
                self.link = True
            else:
                with open(self.fullpath, "rb") as f:
                    sbuf = f.read()
        else:
            sbuf = b""

        t = open(self.fullpath, "wb")
        return apply_txdelta_handler(sbuf, target_stream=t)

    def close(self):
        """When done with the file, this is called.

        So the file exists and is updated, we can:

        - adapt accordingly its execution flag if any
        - compute the objects' checksums
        - replace the svnlink with a real symlink (for disk
          computation purposes)

        """
        is_link = None

        if self.link:
            # can only check now that the link is a real one
            # since patch has been applied
            is_link, src = is_file_an_svnlink_p(self.fullpath)
            if is_link:
                self.__make_symlink(src)
            else:  # not a real link ...
                self.link = False
                # when a file with the svn:special property set is not a svn link,
                # the svn export operation will extract a truncated version of that file
                # if it contains a null byte (see create_special_file_from_stream
                # implementation in libsvn_subr/subst.c), so ensure to produce the
                # same file as the export operation.
                with open(self.fullpath, "rb") as f:
                    content = f.read()
                with open(self.fullpath, "wb") as f:
                    exported_data = content.split(b"\x00")[0]
                    if exported_data != content:
                        # keep track of original file content in order to restore
                        # it if the svn:special property gets unset in another revision
                        self.state.svn_special_path_non_link_data = content
                    f.write(exported_data)
        elif os.path.islink(self.fullpath):
            # path was a symbolic link in previous revision but got the property
            # svn:special unset in current one, revert its content to svn link format
            self.__make_svnlink()
        elif self.state.svn_special_path_non_link_data is not None:
            # path was a non link file with the svn:special property previously set
            # and got truncated on export, restore its original content
            with open(self.fullpath, "wb") as f:
                f.write(self.state.svn_special_path_non_link_data)
                self.state.svn_special_path_non_link_data = None

        if not is_link:  # if a link, do nothing regarding flag
            if self.executable == EXEC_FLAG:
                os.chmod(self.fullpath, 0o755)
            elif self.executable == NOEXEC_FLAG:
                os.chmod(self.fullpath, 0o644)

        # And now compute file's checksums
        if self.state.eol_style and not is_link:
            # ensure to normalize line endings as defined by svn:eol-style
            # property to get the same file checksum as after an export
            # or checkout operation with subversion
            with open(self.fullpath, "rb") as f:
                data = f.read()
                data = _normalize_line_endings(data, self.state.eol_style)
                mode = os.lstat(self.fullpath).st_mode
                self.directory[self.path] = from_disk.Content.from_bytes(
                    mode=mode, data=data
                )
        else:
            self.directory[self.path] = from_disk.Content.from_file(path=self.fullpath)


class BaseDirEditor:
    """Base class implementation of dir editor.

    see :class:`DirEditor` for an implementation that hashes every
    directory encountered.

    Instantiate a new class inheriting from this class and define the following
    functions::

        def update_checksum(self):
            # Compute the checksums at current state

        def open_directory(self, *args):
            # Update an existing folder.

        def add_directory(self, *args):
            # Add a new one.

    """

    __slots__ = ["directory", "rootpath"]

    def __init__(self, directory, rootpath, file_states: Dict[str, FileState]):
        self.directory = directory
        self.rootpath = rootpath
        # build directory on init
        os.makedirs(rootpath, exist_ok=True)
        self.file_states = file_states

    def remove_child(self, path):
        """Remove a path from the current objects.

        The path can be resolved as link, file or directory.

        This function takes also care of removing the link between the
        child and the parent.

        Args:
            path: to remove from the current objects.

        """
        try:
            entry_removed = self.directory[path]
        except KeyError:
            entry_removed = None
        else:
            del self.directory[path]
            fpath = os.path.join(self.rootpath, path)
            if isinstance(entry_removed, from_disk.Directory):
                shutil.rmtree(fpath)
            else:
                os.remove(fpath)

        # when deleting a directory ensure to remove any svn property for the
        # file it contains as they can be added again later in another revision
        # without the same property set
        fullpath = os.path.join(self.rootpath, path)
        for state_path in list(self.file_states):
            if state_path.startswith(fullpath + b"/"):
                del self.file_states[state_path]

    def update_checksum(self):
        raise NotImplementedError("This should be implemented.")

    def open_directory(self, *args):
        raise NotImplementedError("This should be implemented.")

    def add_directory(self, *args):
        raise NotImplementedError("This should be implemented.")

    def open_file(self, *args):
        """Updating existing file.

        """
        path = os.fsencode(args[0])
        self.directory[path] = from_disk.Content()
        fullpath = os.path.join(self.rootpath, path)
        return FileEditor(
            self.directory,
            rootpath=self.rootpath,
            path=path,
            state=self.file_states[fullpath],
        )

    def add_file(self, path, copyfrom_path=None, copyfrom_rev=-1):
        """Creating a new file.

        """
        path = os.fsencode(path)
        self.directory[path] = from_disk.Content()
        fullpath = os.path.join(self.rootpath, path)
        self.file_states[fullpath] = FileState()
        return FileEditor(
            self.directory, self.rootpath, path, state=self.file_states[fullpath]
        )

    def change_prop(self, key, value):
        """Change property callback on directory.

        """
        if key == properties.PROP_EXTERNALS:
            raise ValueError("Property '%s' detected. Not implemented yet." % key)

    def delete_entry(self, path, revision):
        """Remove a path.

        """
        fullpath = os.path.join(self.rootpath, path.encode("utf-8"))
        self.file_states.pop(fullpath, None)
        self.remove_child(path.encode("utf-8"))

    def close(self):
        """Function called when we finish walking a repository.

        """
        self.update_checksum()


class DirEditor(BaseDirEditor):
    """Directory Editor in charge of updating directory hashes computation.

    This implementation includes empty folder in the hash computation.

    """

    def update_checksum(self):
        """Update the root path self.path's checksums according to the
        children's objects.

        This function is expected to be called when the folder has
        been completely 'walked'.

        """
        pass

    def open_directory(self, *args):
        """Updating existing directory.

        """
        return self

    def add_directory(self, path, copyfrom_path=None, copyfrom_rev=-1):
        """Adding a new directory.

        """
        path = os.fsencode(path)
        os.makedirs(os.path.join(self.rootpath, path), exist_ok=True)
        self.directory[path] = from_disk.Directory()
        return self


class Editor:
    """Editor in charge of replaying svn events and computing objects
       along.

       This implementation accounts for empty folder during hash
       computations.

    """

    def __init__(self, rootpath, directory):
        self.rootpath = rootpath
        self.directory = directory
        self.file_states: Dict[str, FileState] = {}

    def set_target_revision(self, revnum):
        pass

    def abort(self):
        pass

    def close(self):
        pass

    def open_root(self, base_revnum):
        return DirEditor(
            self.directory, rootpath=self.rootpath, file_states=self.file_states
        )


class Replay:
    """Replay class.
    """

    def __init__(self, conn, rootpath, directory=None):
        self.conn = conn
        self.rootpath = rootpath
        if directory is None:
            directory = from_disk.Directory()
        self.directory = directory
        self.editor = Editor(rootpath=rootpath, directory=directory)

    def replay(self, rev):
        """Replay svn actions between rev and rev+1.

        This method updates in place the self.editor.directory, as well as the
        filesystem.

        Returns:
           The updated root directory

        """
        codecs.register_error("strict", _ra_codecs_error_handler)
        self.conn.replay(rev, rev + 1, self.editor)
        codecs.register_error("strict", codecs.strict_errors)
        return self.editor.directory

    def compute_objects(
        self, rev: int
    ) -> Tuple[List[Content], List[SkippedContent], List[Directory]]:
        """Compute objects at revisions rev.
        Expects the state to be at previous revision's objects.

        Args:
            rev: The revision to start the replay from.

        Returns:
            The updated objects between rev and rev+1. Beware that this
            mutates the filesystem at rootpath accordingly.

        """
        self.replay(rev)
        return from_disk.iter_directory(self.directory)


@click.command()
@click.option("--local-url", default="/tmp", help="local svn working copy")
@click.option(
    "--svn-url",
    default="file:///home/storage/svn/repos/pkg-fox",
    help="svn repository's url.",
)
@click.option(
    "--revision-start",
    default=1,
    type=click.INT,
    help="svn repository's starting revision.",
)
@click.option(
    "--revision-end",
    default=-1,
    type=click.INT,
    help="svn repository's ending revision.",
)
@click.option(
    "--debug/--nodebug",
    default=True,
    help="Indicates if the server should run in debug mode.",
)
@click.option(
    "--cleanup/--nocleanup",
    default=True,
    help="Indicates whether to cleanup disk when done or not.",
)
def main(local_url, svn_url, revision_start, revision_end, debug, cleanup):
    """Script to present how to use Replay class.

    """
    conn = RemoteAccess(svn_url.encode("utf-8"), auth=Auth([get_username_provider()]))

    os.makedirs(local_url, exist_ok=True)

    rootpath = tempfile.mkdtemp(
        prefix=local_url, suffix="-" + os.path.basename(svn_url)
    )

    rootpath = os.fsencode(rootpath)

    # Do not go beyond the repository's latest revision
    revision_end_max = conn.get_latest_revnum()
    if revision_end == -1:
        revision_end = revision_end_max

    revision_end = min(revision_end, revision_end_max)

    try:
        replay = Replay(conn, rootpath)

        for rev in range(revision_start, revision_end + 1):
            contents, skipped_contents, directories = replay.compute_objects(rev)
            print(
                "r%s %s (%s new contents, %s new directories)"
                % (
                    rev,
                    hashutil.hash_to_hex(replay.directory.hash),
                    len(contents) + len(skipped_contents),
                    len(directories),
                )
            )

        if debug:
            print("%s" % rootpath.decode("utf-8"))
    finally:
        if cleanup:
            if os.path.exists(rootpath):
                shutil.rmtree(rootpath)


if __name__ == "__main__":
    main()
