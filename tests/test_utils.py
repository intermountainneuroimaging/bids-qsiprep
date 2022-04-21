"""Module to test parser.py"""

import json
from os import path as op
from os import symlink

import pytest

from utils import dry_run
from utils.fly import environment


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


def test_get_and_log_environment(tmpdir):
    """Tests for get_and_log_environment

    We'll grab some dict (mocked_gear_options) and save it in a file.
    Then, we call get_and_log_environment and the returned dictionary should be the same as the original.
    """

    mocked_environ_file = tmpdir / "mocked_environ.json"
    # get_and_log_environment only works when the dict values are str:
    mocked_environ = {
        "First_Name": "Jason",
        "Last_Name": "Bourne",
        "Program": "Treadstone",
    }

    # save the mocked_gear_options to the mocked_environ_file:
    with open(mocked_environ_file, "w") as f:
        json.dump(mocked_environ, f)

    # overwrite the ENVIRONMENT_FILE defined in utils.fly.environment:
    environment.ENVIRONMENT_FILE = mocked_environ_file
    env = environment.get_and_log_environment()

    assert env == mocked_environ
