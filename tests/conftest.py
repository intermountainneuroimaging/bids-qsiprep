"""
Set up parameters for testing. Picked up by pytest automatically.
"""

import pytest


@pytest.fixture
def mocked_gear_options():
    return {
        "bids-app-modalities": ["foo", "bar"],
        "dry-run": False,
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
