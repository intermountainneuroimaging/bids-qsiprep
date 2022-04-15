"""Module to test post.py"""

from pathlib import Path

from fw_gear_bids_qsiprep.post import post_run


# mocked_gear_options is defined in conftest.py
def test_post_run(mocked_gear_options):

    """Unit tests for post_run"""

    post_run(
        gear_name=f"foo",
        gear_options=mocked_gear_options,
        analysis_output_dir=Path(f"bar"),
        run_label=f"fum",
        errors=[],
        warnings=[],
    )

    pass
