"""Module to test parser.py"""

from unittest.mock import MagicMock

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_bids_qsiprep.parser import parse_config

# Some config keys we want in the gear_options and app_options:
desired_gear_options = {
    "gear-dry-run": True,
    "gear-keep-output": False,
}
desired_app_options = {"infant": True, "template": "T1w"}

# Options we should ignore:
bad_options = {"bad-option-1": True}


def test_parse_config(tmpdir):
    """Unit tests for `parse_config`"""

    # Note: move to a clean folder, in case the call to GearToolkitContext picks
    # the manifest or configuration.
    tmpdir.chdir()

    ###    create a dummy gear context:   ###

    with GearToolkitContext(input_args=[]) as gear_context:

        # Mock the get_input_path() method:
        gear_context.get_input_path = MagicMock()

        for my_dict in [desired_gear_options, desired_app_options, bad_options]:
            for key, value in my_dict.items():
                gear_context.config[key] = value

        ###   call the parser:   ###

        debug, gear_opt, app_opt = parse_config(gear_context)

        ###   run the checks:   ###

        # Check that we get all that we expected and only what we expected:
        for desired_key, desired_value in desired_gear_options.items():
            # For the gear options, "gear-" should be removed from the key:
            expected_key = desired_key.split("gear-")[1]
            assert gear_opt[expected_key] == desired_value

        for desired_key, desired_value in desired_app_options.items():
            assert app_opt[desired_key] == desired_value

        for bad_key in bad_options:
            assert bad_key not in gear_opt and bad_key not in app_opt

        # list the expected calls to "context.get_input_call()":
        expected_get_input_path_calls = [
            "freesurfer_license",
            "recon-spec",
            "eddy-config",
        ]
        assert gear_context.get_input_path.call_count == len(
            expected_get_input_path_calls
        )

        # Make sure the input args "recon-spec" and "eddy-config" get return in app_options
        # we skip the "freesurfer_license" because its key is "freesurfer-license-path"
        for input_path in expected_get_input_path_calls[1:]:
            # if there was an input path in the context, it should be present in the app_options:
            if gear_context.get_input_path(input_path):
                assert input_path in app_opt
