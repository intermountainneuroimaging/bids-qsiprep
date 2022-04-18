"""Module to test run.py"""
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flywheel_gear_toolkit import GearToolkitContext

import run


# Test 2 use cases:
# - download_bids_for_runlevel returns an error: True/None
@pytest.mark.parametrize("download_bids_for_runlevel_error", [True, False])
def test_get_bids_data(mocked_gear_options, download_bids_for_runlevel_error):
    """Unit tests for get_bids_data"""

    mocked_context = MagicMock(
        spec=GearToolkitContext,
        client="",
        destination={"id": mocked_gear_options["destination-id"]},
    )

    expected_run_label = "foo_label"
    run.get_analysis_run_level_and_hierarchy = MagicMock(
        return_value={"run_label": expected_run_label}
    )
    download_bids_for_runlevel_return_value = 0
    expected_errors = []
    if download_bids_for_runlevel_error:
        download_bids_for_runlevel_return_value = 1
        expected_errors = ["BIDS Error(s) detected"]

    run.download_bids_for_runlevel = MagicMock(
        return_value=download_bids_for_runlevel_return_value
    )

    run_label, errors = run.get_bids_data(
        mocked_context, mocked_gear_options, "my_tree_title"
    )

    assert run_label == expected_run_label
    assert errors == expected_errors
    run.get_analysis_run_level_and_hierarchy.assert_called_once()
    run.download_bids_for_runlevel.assert_called_once()


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
