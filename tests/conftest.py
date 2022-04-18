"""
Set up parameters for testing. Picked up by pytest automatically.
"""

import pytest


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


"""
from unittest.mock import MagicMock



@pytest.fixture
def mock_context(mocker):
    mocker.patch("flywheel_gear_toolkit.GearToolkitContext")
    gtk = MagicMock(
        autospec=True,
        config={
            "gear-ignore-bids-errors": True,
        },
    )
    return gtk
"""

"""
@pytest.fixture
def common_mocks(mocker):
    mock_get = mocker.patch("flywheel_gear_toolkit.GearToolkitContext.config.get")

    return mock_get
"""
