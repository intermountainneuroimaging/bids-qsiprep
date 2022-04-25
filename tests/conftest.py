"""
Set up parameters for testing. Picked up by pytest automatically.
"""

from unittest.mock import MagicMock

import pytest
from flywheel_gear_toolkit import GearToolkitContext


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


"""
@pytest.fixture
def common_mocks(mocker):
    mock_get = mocker.patch("flywheel_gear_toolkit.GearToolkitContext.config.get")

    return mock_get
"""
