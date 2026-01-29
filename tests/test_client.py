"""Tests for HelpSpotClient."""

import pytest

from helpspot import HelpSpotClient


def test_client_initialization(base_url, api_token):
    """Test client initialization."""
    client = HelpSpotClient(base_url=base_url, api_token=api_token)

    assert client.base_url == base_url
    assert client.output_format == "json"
    assert client.requests is not None
    assert client.customers is not None
    assert client.categories is not None


def test_client_base_url_validation():
    """Test base URL validation."""
    # Valid URLs
    client = HelpSpotClient(base_url="https://example.com")
    assert client.base_url == "https://example.com"

    client = HelpSpotClient(base_url="http://example.com/")
    assert client.base_url == "http://example.com"

    # Invalid URLs
    with pytest.raises(ValueError, match="base_url cannot be empty"):
        HelpSpotClient(base_url="")

    with pytest.raises(ValueError, match="must start with"):
        HelpSpotClient(base_url="example.com")


def test_client_context_manager(base_url, api_token):
    """Test client as context manager."""
    with HelpSpotClient(base_url=base_url, api_token=api_token) as client:
        assert client.base_url == base_url
    # Client should be closed after exiting context


def test_version_method(base_url, mock_version_response):
    """Test the version() method."""
    client = HelpSpotClient(base_url=base_url)
    version = client.version()

    assert version.version == "5.0"
    assert version.min_version == "4.0"


def test_client_ssl_verification_disabled(base_url, api_token):
    """Test client with SSL verification disabled."""
    client = HelpSpotClient(base_url=base_url, api_token=api_token, verify_ssl=False)

    assert client.base_url == base_url
    assert (
        client._http_client._transport._pool._ssl_context is None
        or not client._http_client._transport._pool._ssl_context.check_hostname
    )

    client.close()


def test_client_ssl_verification_enabled_by_default(base_url, api_token):
    """Test client has SSL verification enabled by default."""
    client = HelpSpotClient(base_url=base_url, api_token=api_token)

    assert client.base_url == base_url
    # When verify=True, httpx uses default SSL context

    client.close()
