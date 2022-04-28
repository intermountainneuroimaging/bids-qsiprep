"""Module to test run.py"""
import logging
import os
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


# Test 2x2 use cases:
# - save_intermediate_output: True/False
@pytest.mark.parametrize("save_intermediate_output", [True, False])
# - keep_output: True/False
@pytest.mark.parametrize("keep_output", [True, False])
def test_post_run(
    tmpdir, caplog, mocked_gear_options, save_intermediate_output, keep_output
):
    """Test the post_run method"""

    logging.getLogger(__name__)
    caplog.set_level(logging.INFO)

    this_gear_options = mocked_gear_options
    this_gear_options["save-intermediate-output"] = save_intermediate_output
    this_gear_options["keep-output"] = keep_output
    this_gear_options["work-dir"] = "work"
    this_gear_options["intermediate-files"] = ""
    this_gear_options["intermediate-folders"] = ""

    gear_name = "Mocked_gear"
    analysis_output_dir = tmpdir / "mocked_outdir"
    mocked_errors = ["error 1", "error 2", "error 3"]
    mocked_warnings = ["warning 1", "warning 2"]

    # make analysis_output_dir (to later check if it was removed)
    os.mkdir(analysis_output_dir)

    run.zip_output = MagicMock()
    run.zip_htmls = MagicMock()
    run.zip_all_intermediate_output = MagicMock()
    run.zip_intermediate_selected = MagicMock()

    run.post_run(
        gear_name,
        this_gear_options,
        analysis_output_dir,
        "mocked_run_label",
        mocked_errors,
        mocked_warnings,
    )

    run.zip_output.assert_called_once()
    run.zip_htmls.assert_called_once()
    run.zip_intermediate_selected.assert_called_once()
    if save_intermediate_output:
        run.zip_all_intermediate_output.assert_called_once()
    else:
        run.zip_all_intermediate_output.assert_not_called()

    if keep_output:
        assert os.path.isdir(analysis_output_dir)
        assert "NOT removing output directory" in caplog.text
    else:
        assert not os.path.isdir(analysis_output_dir)

    # Make sure there is a "Previous warnings" entry in the log, with a list of the mocked_warnings:
    assert ["Previous warnings" in l.message for l in caplog.records]
    warning_log_entry = [
        l.message for l in caplog.records if "Previous warnings" in l.message
    ][0]
    for e in mocked_warnings:
        assert e in warning_log_entry

    # Make sure there is a "Previous errors" entry in the log, with a list of the mocked_errors:
    assert ["Previous errors" in l.message for l in caplog.records]
    error_log_entry = [
        l.message for l in caplog.records if "Previous errors" in l.message
    ][0]
    for e in mocked_errors:
        assert e in error_log_entry


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
