#!/usr/bin/env python
"""The run script"""
import logging
import sys

from flywheel_gear_toolkit import GearToolkitContext

# This design with the main interfaces separated from a gear module (with main and parser)
# allows the gear module to be publishable, so it can then be imported in another project,
# which enables chaining multiple gears together.
from fw_gear_bids_qsiprep.main import run
from fw_gear_bids_qsiprep.parser import parse_config

# The gear is split up into 2 main components. The run.py file which is executed
# when the container runs. The run.py file then imports the rest of the gear as a
# module.


log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parses config and run"""

    # Call the fw_gear_bids_qsiprep.parser.parse_config function
    # to extract the args, kwargs from the context (e.g. config.json).
    debug, gear_options, app_options = parse_config(context)

    # Pass the args, kwargs to fw_gear_qsiprep.main.run function to execute
    # the main functionality of the gear.
    e_code = run(gear_options, app_options)

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
