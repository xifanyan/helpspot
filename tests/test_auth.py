"""Tests for authentication."""

import httpx
import pytest

from helpspot import HelpSpotClient
from helpspot.auth import BearerAuth


def test_bearer_auth_initialization():
    """Test BearerAuth initialization."""
    token = "1|test_token"
    auth = BearerAuth(token)
    assert auth.token == token


def test_bearer_auth_adds_header():
    """Test that BearerAuth adds Authorization header."""
    token = "1|test_token"
    auth = BearerAuth(token)

    # Create a mock request
    request = httpx.Request("GET", "https://example.com")

    # Apply auth
    auth_flow = auth.auth_flow(request)
    next(auth_flow)

    assert request.headers["Authorization"] == f"Bearer {token}"


def test_client_with_api_token(base_url, api_token):
    """Test client initialization with API token."""
    client = HelpSpotClient(base_url=base_url, api_token=api_token)

    assert client.base_url == base_url
    assert isinstance(client.auth, BearerAuth)


def test_client_with_basic_auth(base_url):
    """Test client initialization with basic auth."""
    client = HelpSpotClient(base_url=base_url, username="user@example.com", password="password123")

    assert client.base_url == base_url
    assert isinstance(client.auth, httpx.BasicAuth)


def test_client_without_auth(base_url):
    """Test client initialization without authentication."""
    client = HelpSpotClient(base_url=base_url)

    assert client.base_url == base_url
    assert client.auth is None


def test_client_basic_auth_incomplete(base_url):
    """Test that incomplete basic auth raises error."""
    with pytest.raises(ValueError, match="Both username and password"):
        HelpSpotClient(base_url=base_url, username="user@example.com")

    with pytest.raises(ValueError, match="Both username and password"):
        HelpSpotClient(base_url=base_url, password="password123")
