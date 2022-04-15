"""Module to test run.py"""
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flywheel_gear_toolkit import GearToolkitContext

import run


def test_get_bids_data(mocked_gear_options):
    """Unit tests for get_bids_data"""

    mocked_context = MagicMock(spec=GearToolkitContext)

    expected_run_label = f"foo"
    expected_errors = []

    run_label, errors = run.get_bids_data(
        mocked_context, mocked_gear_options, f"my_tree_title"
    )

    assert run_label == expected_run_label
    assert errors == expected_errors


def test_main(mocked_gear_options):
    """Unit tests for main"""

    mocked_manifest = {
        "name": "test",
        "custom": {"gear-builder": {"image": "foo/bar:v1.0"}},
    }
    mocked_context = MagicMock(spec=run.GearToolkitContext, manifest=mocked_manifest)
    mocked_parse_config_return = (False, mocked_gear_options, {})

    run.parse_config = MagicMock(return_value=mocked_parse_config_return)
    run.install_freesurfer_license = MagicMock()
    run.prepare = MagicMock(return_value=([], []))
    run.get_bids_data = MagicMock(return_value=(f"foo", []))
    run.run = MagicMock(return_value=0)
    run.post_run = MagicMock()

    with pytest.raises(SystemExit):
        run.main(mocked_context)

    run.install_freesurfer_license.assert_called_once()
