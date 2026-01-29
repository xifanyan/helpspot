"""Test configuration and fixtures."""

import json
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def base_url() -> str:
    """Base URL for test HelpSpot installation."""
    return "https://test.helpspot.com"


@pytest.fixture
def api_token() -> str:
    """Test API token."""
    return "1|test_token_12345"


@pytest.fixture
def load_fixture():
    """Load a JSON fixture file."""

    def _load(filename: str) -> dict:
        fixture_path = FIXTURES_DIR / filename
        with open(fixture_path) as f:
            return json.load(f)

    return _load


@pytest.fixture
def mock_version_response(httpx_mock: HTTPXMock, load_fixture):
    """Mock the version API response."""
    httpx_mock.add_response(
        url="https://test.helpspot.com/api/index.php?method=version&output=json",
        json=load_fixture("version.json"),
    )


@pytest.fixture
def mock_request_get_response(httpx_mock: HTTPXMock, load_fixture):
    """Mock the request.get API response."""
    httpx_mock.add_response(
        url="https://test.helpspot.com/api/index.php?method=private.request.get&xRequest=12745&output=json",
        json=load_fixture("request_get.json"),
    )
