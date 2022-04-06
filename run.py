#!/usr/bin/env python
"""The run script"""
import logging
import sys
from pathlib import Path
from typing import List, Tuple

from flywheel_gear_toolkit import GearToolkitContext

# This design with the main interfaces separated from a gear module (with main and parser)
# allows the gear module to be publishable, so it can then be imported in another project,
# which enables chaining multiple gears together.
from fw_gear_bids_qsiprep.main import prepare, run
from fw_gear_bids_qsiprep.parser import parse_config

# The gear is split up into 2 main components. The run.py file which is executed
# when the container runs. The run.py file then imports the rest of the gear as a
# module.

GEAR = "bids-qsiprep"
REPO = "flywheel-apps"
CONTAINER = f"{REPO}/{GEAR}]"

log = logging.getLogger(__name__)

BIDS_APP = "qsiprep"


def get_bids_data(
    context: GearToolkitContext,
    gear_options: dict,
    tree_title: str,
) -> Tuple[str, List[str]]:
    """Get the data in BIDS structure.
    It returns any error found downloading the BIDS data

    For FW gears, it downloads the data
    For RL containers, it just points/links to the storage folder
    It should be independent of the specific BIDS-App

    Args:
        context (GearToolkitContext): gear context
        gear_options (Dict): gear options
        tree_title (str): title for the BIDS tree

    Returns:
        run_label (str): run label
        errors (list[str]): list of generated errors
    """

    run_label = f"foo"
    errors = []

    return run_label, errors


def post_run(
    gear_name: str,
    gear_options: dict,
    analysis_output_dir: Path,
    run_label: str,
    errors: List[str],
    warnings: List[str],
):
    """Move all the results to the final destination, write out any
    metadata, clean-up, etc.

    Different for FW and RL instances
    Parts might be BIDS-App specific (the results), parts will be common
    (reporting errors, clean-up, etc.)
    """

    # do nothing, for now
    pass


def main(context: GearToolkitContext) -> None:
    """Parses config and run"""

    # Errors and warnings will always be logged when they are detected.
    # Keep a list of errors and warning to print all in one place at end of log
    # Any errors will prevent the BIDS App from running.
    errors = []
    warnings = []

    # Call the fw_gear_bids_qsiprep.parser.parse_config function
    # to extract the args, kwargs from the context (e.g. config.json).
    debug, gear_options, app_options = parse_config(context)

    command, prepare_errors, prepare_warnings = prepare(
        gear_options=gear_options,
        app_options=app_options,
    )
    errors.append(prepare_errors)
    warnings.append(prepare_warnings)

    run_label, get_bids_errors = get_bids_data(
        context=context,
        gear_options=gear_options,
        tree_title=f"BIDS-QSIPrep",
    )
    errors.append(get_bids_errors)

    # Pass the args, kwargs to fw_gear_qsiprep.main.run function to execute
    # the main functionality of the gear.
    e_code = run(gear_options, app_options)

    # Cleanup, move all results to the output directory
    post_run(
        gear_name=context.manifest["name"],
        gear_options=gear_options,
        analysis_output_dir=f"output_analysis_placeholder",
        run_label=run_label,
        errors=errors,
        warnings=warnings,
    )

    log.info("%s Gear is done.  Returning %s", CONTAINER, e_code)

    # Exit the python script (and thus the container) with the exit
    # code returned by fw_gear_bids_qsiprep.main.run function.
    sys.exit(e_code)


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:

        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()

        # Pass the gear context into main function defined above.
        main(gear_context)
