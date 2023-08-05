# Copyright (C) 2016-2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import logging
import os
import pty
import shutil
from subprocess import Popen

from swh.loader.svn import utils
from swh.model.model import Timestamp


def test_outputstream():
    stdout_r, stdout_w = pty.openpty()
    echo = Popen(["echo", "-e", "foo\nbar\nbaz"], stdout=stdout_w)
    os.close(stdout_w)
    stdout_stream = utils.OutputStream(stdout_r)
    lines = []
    while True:
        current_lines, readable = stdout_stream.read_lines()
        lines += current_lines
        if not readable:
            break
    echo.wait()
    os.close(stdout_r)
    assert lines == ["foo", "bar", "baz"]


def test_strdate_to_timestamp():
    """Formatted string date should be converted in timestamp."""
    actual_ts = utils.strdate_to_timestamp("2011-05-31T06:04:39.800722Z")
    assert actual_ts == Timestamp(seconds=1306821879, microseconds=800722)

    actual_ts = utils.strdate_to_timestamp("2011-05-31T06:03:39.123450Z")
    assert actual_ts == Timestamp(seconds=1306821819, microseconds=123450)


def test_strdate_to_timestamp_empty_does_not_break():
    """Empty or None date should be timestamp 0."""
    default_ts = Timestamp(seconds=0, microseconds=0)
    assert default_ts == utils.strdate_to_timestamp("")
    assert default_ts == utils.strdate_to_timestamp(None)


def test_init_svn_repo_from_dump(datadir, tmp_path):
    """Mounting svn repository out of a dump is ok"""
    dump_name = "penguinsdbtools2018.dump.gz"
    dump_path = os.path.join(datadir, dump_name)

    tmp_repo, repo_path = utils.init_svn_repo_from_dump(
        dump_path, gzip=True, cleanup_dump=False, root_dir=tmp_path
    )

    assert os.path.exists(dump_path), "Dump path should still exists"
    assert os.path.exists(repo_path), "Repository should exists"


def test_init_svn_repo_from_dump_and_cleanup(datadir, tmp_path):
    """Mounting svn repository with a dump cleanup after is ok"""
    dump_name = "penguinsdbtools2018.dump.gz"
    dump_ori_path = os.path.join(datadir, dump_name)

    dump_path = os.path.join(tmp_path, dump_name)
    shutil.copyfile(dump_ori_path, dump_path)

    assert os.path.exists(dump_path)
    assert os.path.exists(dump_ori_path)

    tmp_repo, repo_path = utils.init_svn_repo_from_dump(
        dump_path, gzip=True, root_dir=tmp_path
    )

    assert not os.path.exists(dump_path), "Dump path should no longer exists"
    assert os.path.exists(repo_path), "Repository should exists"
    assert os.path.exists(dump_ori_path), "Original dump path should still exists"


def test_init_svn_repo_from_dump_and_cleanup_already_done(
    datadir, tmp_path, mocker, caplog
):
    """Mounting svn repository out of a dump is ok"""
    caplog.set_level(logging.INFO, "swh.loader.svn.utils")

    dump_name = "penguinsdbtools2018.dump.gz"
    dump_ori_path = os.path.join(datadir, dump_name)

    mock_remove = mocker.patch("os.remove")
    mock_remove.side_effect = FileNotFoundError

    dump_path = os.path.join(tmp_path, dump_name)
    shutil.copyfile(dump_ori_path, dump_path)

    assert os.path.exists(dump_path)
    assert os.path.exists(dump_ori_path)

    tmp_repo, repo_path = utils.init_svn_repo_from_dump(
        dump_path, gzip=True, root_dir=tmp_path
    )

    assert os.path.exists(repo_path), "Repository should exists"
    assert os.path.exists(dump_ori_path), "Original dump path should still exists"

    assert len(caplog.record_tuples) == 1
    assert "Failure to remove" in caplog.record_tuples[0][2]
    assert mock_remove.called


def test_init_svn_repo_from_archive_dump(datadir, tmp_path):
    """Mounting svn repository out of an archive dump is ok"""
    dump_name = "penguinsdbtools2018.dump.gz"
    dump_path = os.path.join(datadir, dump_name)

    tmp_repo, repo_path = utils.init_svn_repo_from_archive_dump(
        dump_path, cleanup_dump=False, root_dir=tmp_path
    )

    assert os.path.exists(dump_path), "Dump path should still exists"
    assert os.path.exists(repo_path), "Repository should exists"


def test_init_svn_repo_from_archive_dump_and_cleanup(datadir, tmp_path):
    """Mounting svn repository out of a dump is ok"""
    dump_name = "penguinsdbtools2018.dump.gz"
    dump_ori_path = os.path.join(datadir, dump_name)

    dump_path = os.path.join(tmp_path, dump_name)
    shutil.copyfile(dump_ori_path, dump_path)

    assert os.path.exists(dump_path)
    assert os.path.exists(dump_ori_path)

    tmp_repo, repo_path = utils.init_svn_repo_from_archive_dump(
        dump_path, root_dir=tmp_path
    )

    assert not os.path.exists(dump_path), "Dump path should no longer exists"
    assert os.path.exists(repo_path), "Repository should exists"
    assert os.path.exists(dump_ori_path), "Original dump path should still exists"
