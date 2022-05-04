"""
Set up parameters for testing. Picked up by pytest automatically.
"""

import shutil
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils.zip_tools import unzip_archive


@pytest.fixture
def mocked_gear_options():
    return {
        "bids-app-binary": "f00_binary",
        "bids-app-modalities": ["foo", "bar"],
        "dry-run": False,
        "output-dir": "classified",
        "destination-id": "also_classified",
        "run-bids-validation": False,
        "ignore-bids-errors": False,
    }


@pytest.fixture
def mocked_context(mocked_gear_options):
    """Return a mocked GearToolkitContext"""
    mocked_manifest = {
        "name": "test",
        "custom": {"gear-builder": {"image": "foo/bar:v1.0"}},
    }
    return MagicMock(
        spec=GearToolkitContext,
        manifest=mocked_manifest,
        client="",
        destination={"id": mocked_gear_options["destination-id"]},
    )


FWV0 = Path.cwd()


@pytest.fixture
def install_gear_results():
    def _method(zip_name, gear_output_dir=None):
        """Un-archive gear results to simulate running inside a real gear.

        This will delete and then install: config.json input/ output/ work/ freesurfer/

        Args:
            zip_name (str): name of zip file that holds simulated gear.
            gear_output_dir (str): where to install the contents of the zipped file
        """

        # location of the zip file:
        gear_tests = Path("/src/tests/data/")
        if not gear_tests.exists():  # fix for running in circleci
            gear_tests = FWV0 / "tests" / "data/"

        # where to install the data
        if not gear_output_dir or not Path(gear_output_dir).exists():
            gear_output_dir = FWV0

        print("\nRemoving previous gear...")

        if Path(gear_output_dir / "config.json").exists():
            Path(gear_output_dir / "config.json").unlink()

        for dir_name in ["input", "output", "work", "freesurfer"]:
            path = Path(gear_output_dir / dir_name)
            if path.exists():
                print(f"shutil.rmtree({str(path)}")
                shutil.rmtree(path)

        print(f'\ninstalling new gear, "{zip_name}"...')
        unzip_archive(gear_tests / zip_name, str(gear_output_dir))

        # The "freesurfer" directory needs to have the standard freesurfer
        # "subjects" directory and "license.txt" file.

    return _method
