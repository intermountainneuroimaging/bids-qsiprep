#!/usr/bin/env python
"""The run script"""
import logging
import sys

from flywheel_gear_toolkit import GearToolkitContext

# This design with a separate main and parser module
# allows the gear to be publishable and the main interfaces
# to it can then be imported in another project which enables
# chaining multiple gears together.
from fw_gear_bids_qsiprep.main import run
from fw_gear_bids_qsiprep.parser import parse_config

# The run.py should be as minimal as possible.
# The gear is split up into 2 main components. The run.py file which is executed
# when the container runs. The run.py file then imports the rest of the gear as a
# module.


log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parses config and run"""

    # Call the fw_gear_skeleton.parser.parse_config function
    # to extract the args, kwargs from the context (e.g. config.json).
    debug, text = parse_config(context)

    # Pass the args, kwargs to fw_gear_skeleton.main.run function to execute
    # the main functionality of the gear.
    e_code = run(text)

    # Exit the python script (and thus the container) with the exit
    # code returned by example_gear.main.run function.
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
