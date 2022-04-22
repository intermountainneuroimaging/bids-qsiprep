"""Module to test run.py"""
import logging
from unittest.mock import MagicMock

import pytest
from flywheel_gear_toolkit import GearToolkitContext

import run


# Test 2 use cases:
# - download_bids_for_runlevel returns an error: True/None
@pytest.mark.parametrize("download_bids_for_runlevel_error", [True, False])
def test_get_bids_data(
    mocked_context, mocked_gear_options, download_bids_for_runlevel_error
):
    """Unit tests for get_bids_data"""

    base_run_label = "foo_label"
    # introduce a forbidden character ("*") to make sure it gets sanitized:
    invalid_run_label = base_run_label + "*"
    expected_run_label = base_run_label + "star"
    run.get_analysis_run_level_and_hierarchy = MagicMock(
        return_value={"run_label": invalid_run_label}
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


# Test 4 use cases:
# - errors: None/prepare_errors/get_bids_data_errors/run_errors
@pytest.mark.parametrize(
    "errors", [None, "prepare_errors", "get_bids_data_errors", "run_errors"]
)
def test_main(caplog, mocked_gear_options, mocked_context, errors):
    """Unit tests for main"""

    logging.getLogger(__name__)
    caplog.set_level(logging.INFO)

    mocked_parse_config_return = (False, mocked_gear_options, {})

    run.parse_config = MagicMock(return_value=mocked_parse_config_return)
    run.install_freesurfer_license = MagicMock()
    if errors == "prepare_errors":
        run.prepare = MagicMock(return_value=([errors], []))
    else:
        run.prepare = MagicMock(return_value=([], []))

    if errors == "get_bids_data_errors":
        run.get_bids_data = MagicMock(return_value=(f"foo", [errors]))
    else:
        run.get_bids_data = MagicMock(return_value=(f"foo", []))

    if errors == "run_errors":
        run.run = MagicMock(side_effect=RuntimeError(errors))
    else:
        run.run = MagicMock(return_value=0)

    run.post_run = MagicMock()

    with pytest.raises(SystemExit):
        run.main(mocked_context)

    run.install_freesurfer_license.assert_called_once()
    run.prepare.assert_called_once()

    if errors is None:
        run.get_bids_data.assert_called_once()
        run.run.assert_called_once()
        run.post_run.assert_called_once()

    elif errors == "prepare_errors":
        run.get_bids_data.assert_not_called()
        run.run.assert_not_called()
        run.post_run.assert_not_called()
        assert ["Command was NOT run" in l.message for l in caplog.records]

    elif errors == "get_bids_data_errors":
        run.get_bids_data.assert_called_once()
        run.run.assert_not_called()
        run.post_run.assert_not_called()

    elif errors == "run_errors":
        run.get_bids_data.assert_called_once()
        run.run.assert_called_once()
        run.post_run.assert_called_once()
        assert [l.levelno == logging.CRITICAL for l in caplog.records]
