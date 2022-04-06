"""Main module."""

import logging
from typing import List, Tuple

log = logging.getLogger(__name__)


def prepare(
    gear_options: dict,
    app_options: dict,
) -> Tuple[List[str], List[str], List[str]]:
    """Prepare everything for the algorithm run.

    It should:
     - Install FreeSurfer license (if needed)
     - Generate the command that will run the main application

    Same for FW and RL instances.
    Potentially, this could be BIDS-App independent?

    Args:
        gear_options (Dict): gear options
        app_options (Dict): options for the app

    Returns:
        command (list[str]): command generated, as a list of str
        errors (list[str]): list of generated errors
        warnings (list[str]): list of generated warnings
    """

    # TO-DO:
    # -install_freesurfer_license
    # -generate_command

    command = []
    errors = []
    warnings = []

    return command, errors, warnings


def run(gear_options: dict, app_options: dict) -> int:
    """Run QSIPrep itself

    Arguments:
        gear_options: dict with gear-specific options
        app_options: dict with options for the BIDS-App

    Returns:
        run_error: any error encountered running the app. (0: no error)
    """
    log.info("This is the beginning of the run file")

    run_error = 0

    return run_error
