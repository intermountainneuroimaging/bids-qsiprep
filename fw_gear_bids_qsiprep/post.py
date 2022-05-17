"""Post module to handle all of the gear output and cleanup."""

from pathlib import Path
from typing import List


def post_run(
    gear_name: str,
    gear_options: dict,
    analysis_output_dir: Path,
    run_label: str,
    errors: List[str],
    warnings: List[str],
):
    """Final tasks.

    Move all the results to the final destination, write out any metadata, clean-up,...

    Different for FW and RL instances
    Parts might be BIDS-App specific (the results), parts will be common
    (reporting errors, clean-up, etc.)
    """
    # do nothing, for now
    pass
