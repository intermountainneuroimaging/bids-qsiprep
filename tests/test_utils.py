"""Module to test parser.py"""

from os import path as op
from os import symlink

import pytest

from utils import dry_run


def test_make_dirs_and_files(tmpdir):
    """Tests make_dirs_and_files"""

    # test with a string and with a Path:
    files = [str(tmpdir / "foo" / "bar.txt"), tmpdir / "foo" / "fam" / "bar.txt"]

    dry_run.make_dirs_and_files(files)

    assert [op.exists(f) for f in files]


def test_pretend_it_ran(tmpdir):
    """Tests for pretend_it_ran"""

    destination_id = "foo"

    # pretend_it_ran will create the folders "work" and "output" in the WORKDIR (/flywheel/v0).
    # So the files created there are deleted after running the test, link those folders to "tmpdir"
    expected_folders = ["work", "output"]
    for ef in expected_folders:
        symlink(ef, tmpdir / ef)

    dry_run.pretend_it_ran(destination_id)

    assert [op.exists(ef) for f in expected_folders]
    assert op.exists(op.join("output", destination_id, "somedir", "sub-TOME3024.html"))
