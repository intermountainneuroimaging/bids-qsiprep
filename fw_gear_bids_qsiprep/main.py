"""Main module."""

import logging

log = logging.getLogger(__name__)


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
