"""Module to test run.py"""
import logging
import os
from unittest.mock import MagicMock, patch

import pytest

import run

MOCKED_RUN_LABEL = "foo_label"
MOCKED_SUBJECT_LABEL = "sub-Mocked"


# Test 2 use cases:
# - download_bids_for_runlevel returns an error: True/None
@pytest.mark.parametrize("download_bids_for_runlevel_error", [True, False])
@patch("run.get_analysis_run_level_and_hierarchy")
@patch("run.download_bids_for_runlevel")
def test_get_bids_data(
    mock_download_bids_for_runlevel,
    mock_get_analysis_run_level_and_hierarchy,
    mocked_context,
    mocked_gear_options,
    download_bids_for_runlevel_error,
):
    """Unit tests for get_bids_data"""

    # introduce a forbidden character ("*") to make sure it gets sanitized:
    invalid_run_label = MOCKED_RUN_LABEL + "*"
    expected_run_label = MOCKED_RUN_LABEL + "star"
    mocked_hierarchy_dict = {
        "run_label": invalid_run_label,
        "subject_label": MOCKED_SUBJECT_LABEL,
    }
    mock_get_analysis_run_level_and_hierarchy.return_value = mocked_hierarchy_dict
    download_bids_for_runlevel_return_value = 0
    expected_errors = []
    if download_bids_for_runlevel_error:
        download_bids_for_runlevel_return_value = 1
        expected_errors = ["BIDS Error(s) detected"]

    mock_download_bids_for_runlevel.return_value = (
        download_bids_for_runlevel_return_value
    )

    subject_label, run_label, errors = run.get_bids_data(
        mocked_context, mocked_gear_options, "my_tree_title"
    )

    assert subject_label == MOCKED_SUBJECT_LABEL
    # check that the run_label gets sanitized
    assert run_label == expected_run_label
    assert errors == expected_errors
    mock_get_analysis_run_level_and_hierarchy.assert_called_once()
    mock_download_bids_for_runlevel.assert_called_once()


@patch("run.zip_output")
@patch("run.zip_htmls")
@patch("run.zip_all_intermediate_output")
@patch("run.zip_intermediate_selected")
# Test 2x2 use cases:
# - save_intermediate_output: True/False
@pytest.mark.parametrize("save_intermediate_output", [True, False])
# - keep_output: True/False
@pytest.mark.parametrize("keep_output", [True, False])
def test_post_run(
    mock_zip_intermediate_selected,
    mock_zip_all_intermediate_output,
    mock_zip_htmls,
    _,
    tmpdir,
    caplog,
    search_caplog_contains,
    mocked_gear_options,
    save_intermediate_output,
    keep_output,
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

    run.post_run(
        gear_name,
        this_gear_options,
        analysis_output_dir,
        MOCKED_RUN_LABEL,
        mocked_errors,
        mocked_warnings,
    )

    mock_zip_htmls.assert_called_once()
    mock_zip_intermediate_selected.assert_called_once()
    if save_intermediate_output:
        mock_zip_all_intermediate_output.assert_called_once()
    else:
        mock_zip_all_intermediate_output.assert_not_called()

    if keep_output:
        assert os.path.isdir(analysis_output_dir)
        assert search_caplog_contains(caplog, "NOT removing output directory")
    else:
        assert not os.path.isdir(analysis_output_dir)

    # Make sure there is a "Previous warnings" entry in the log, with a list of the
    # mocked_warnings:
    assert all(
        search_caplog_contains(caplog, "Previous warnings", w) for w in mocked_warnings
    )

    # Make sure there is a "Previous errors" entry in the log, with a list of the
    # mocked_errors:
    assert all(
        search_caplog_contains(caplog, "Previous errors", e) for e in mocked_errors
    )


# Test 4 use cases:
# - errors: None/prepare_errors/get_bids_data_errors/run_errors
@pytest.mark.parametrize(
    "errors", [None, "prepare_errors", "get_bids_data_errors", "run_errors"]
)
@patch("run.install_freesurfer_license")
@patch("run.prepare")
@patch("run.get_bids_data")
@patch("run.run")
@patch("run.post_run")
def test_main(
    mock_post_run,
    mock_run,
    mock_get_bids_data,
    mock_prepare,
    mock_install_freesurfer_license,
    caplog,
    search_caplog_contains,
    mocked_gear_options,
    mocked_context,
    errors,
):
    """Unit tests for main"""

    logging.getLogger(__name__)
    caplog.set_level(logging.INFO)

    mocked_gear_options["analysis-level"] = "participant"
    mocked_app_options = {"participant_label": ""}
    mocked_parse_config_return = (mocked_gear_options, mocked_app_options)

    # We expect 'main' to get the subject label from the hierarchy, and strip the
    # "sub-" prefix:
    expected_app_options = {"participant_label": MOCKED_SUBJECT_LABEL[len("sub-") :]}

    if errors == "prepare_errors":
        mock_prepare.return_value = ([errors], [])
    else:
        mock_prepare.return_value = ([], [])

    if errors == "get_bids_data_errors":
        mock_get_bids_data.return_value = (
            MOCKED_SUBJECT_LABEL,
            MOCKED_RUN_LABEL,
            [errors],
        )
    else:
        mock_get_bids_data.return_value = (MOCKED_SUBJECT_LABEL, MOCKED_RUN_LABEL, [])

    if errors == "run_errors":
        mock_run.side_effect = RuntimeError(errors)
    else:
        mock_run.return_value = 0

    with pytest.raises(SystemExit):
        with patch(
            "run.parse_config", MagicMock(return_value=mocked_parse_config_return)
        ):
            run.main(mocked_context)

    mock_install_freesurfer_license.assert_called_once()
    mock_prepare.assert_called_once()

    if errors is None:
        mock_get_bids_data.assert_called_once()
        mock_run.assert_called_once_with(mocked_gear_options, expected_app_options)
        mock_post_run.assert_called_once()

    elif errors == "prepare_errors":
        mock_get_bids_data.assert_not_called()
        mock_run.assert_not_called()
        # when prepare throws an error, we still want to run the `post_run` to return
        # any intermediate files, which might help find what the error was.
        mock_post_run.assert_called()
        assert search_caplog_contains(caplog, "Command was NOT run")

    elif errors == "get_bids_data_errors":
        mock_get_bids_data.assert_called_once()
        mock_run.assert_not_called()
        # when get_bids_data throws an error, we still want to run the `post_run` to
        # return any intermediate files, which might help find what the error was.
        mock_post_run.assert_called()

    elif errors == "run_errors":
        mock_get_bids_data.assert_called_once()
        mock_run.assert_called_once()
        mock_post_run.assert_called_once()
        assert [rec.levelno == logging.CRITICAL for rec in caplog.records]
