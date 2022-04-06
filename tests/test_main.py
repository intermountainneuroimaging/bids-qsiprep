"""Module to test main.py"""
import pytest

from fw_gear_bids_qsiprep import main

mocked_gear_options = {
    "LastName": "Bourne",
    "FirstName": "Jason",
}


def test_prepare():
    """Unit tests for prepare"""

    mocked_gear_options = {
        "LastName": "Bourne",
        "FirstName": "Jason",
    }
    app_options = {}

    expected_command = []
    expected_errors = []
    expected_warnings = []

    my_command, errors, warnings = main.prepare(mocked_gear_options, app_options)

    assert my_command == expected_command
    assert errors == expected_errors
    assert warnings == expected_warnings


def test_run():
    """Unit tests for run"""

    exit_code = main.run([], [])

    assert exit_code == 0
