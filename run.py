#!/usr/bin/env python
"""The run script"""
import logging
import sys
from pathlib import Path
from typing import List, Tuple

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.licenses.freesurfer import install_freesurfer_license

# This design with the main interfaces separated from a gear module (with main and parser)
# allows the gear module to be publishable, so it can then be imported in another project,
# which enables chaining multiple gears together.
from fw_gear_bids_qsiprep.main import prepare, run
from fw_gear_bids_qsiprep.parser import parse_config
from fw_gear_bids_qsiprep.post import post_run

# The gear is split up into 2 main components. The run.py file which is executed
# when the container runs. The run.py file then imports the rest of the gear as a
# module.

log = logging.getLogger(__name__)

BIDS_APP = "qsiprep"

# where the app expects the FS license
# TO-DO: the app expects it in ${FREESURFER_HOME}/license.txt, so we should be
#    reading the variable FREESURFER_HOME from the gear_environ.json
FREESURFER_LICENSE = "/opt/freesurfer/license.txt"


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

    # TO-DO: install_freesurfer_license from the gear_toolkit takes the gear context as an argument,
    #    so it is only valid for FW instances. However, the functionality of taking a FreeSurfer
    #    license (either string or file) and copying it to wherever your app expects it should be
    #    the same whether you run it on FW, or XNAT or HPC or locally.
    #    In the future, it would be great to have a "instance-independent" install_freesurfer_license
    #    and have a "instance-dependent" function to extract the license from the context.
    #    At that point, we could extract the license e.g. in the parser, and this function can be moved
    #    to fw_gear_bids_qsiprep.main
    install_freesurfer_license(context, FREESURFER_LICENSE)

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

    gear_builder = context.manifest.get("custom").get("gear-builder")
    # gear_builder.get("image") should be something like: flywheel/bids-qsiprep:0.0.1_0.15.1
    container = gear_builder.get("image").split(":")[0]
    log.info("%s Gear is done.  Returning %s", container, e_code)

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
