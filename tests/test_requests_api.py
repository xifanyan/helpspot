"""Tests for RequestsAPI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from httpx import Response

from helpspot import HelpSpotClient
from helpspot.exceptions import APIError, ValidationError


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def request_get_data(fixtures_dir: Path) -> dict:
    """Load request.get fixture data."""
    with open(fixtures_dir / "request_get.json") as f:
        return json.load(f)


@pytest.fixture
def request_create_data(fixtures_dir: Path) -> dict:
    """Load request.create fixture data."""
    with open(fixtures_dir / "request_create.json") as f:
        return json.load(f)


@pytest.fixture
def request_search_data(fixtures_dir: Path) -> dict:
    """Load request.search fixture data."""
    with open(fixtures_dir / "request_search.json") as f:
        return json.load(f)


@pytest.fixture
def api_error_data(fixtures_dir: Path) -> dict:
    """Load API error fixture data."""
    with open(fixtures_dir / "api_error.json") as f:
        return json.load(f)


class TestRequestsAPICreate:
    """Tests for RequestsAPI.create()."""

    def test_create_public_api(
        self,
        base_url: str,
        httpx_mock,
        request_create_data: dict,
    ):
        """Test creating a request via public API (no auth)."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=request.create&output=json",
            json=request_create_data,
        )

        client = HelpSpotClient(base_url=base_url)
        request = client.requests.create(
            note="Test note",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

        assert request.x_request == 12750
        assert request.accesskey == "12750abc123"

    def test_create_private_api(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_create_data: dict,
    ):
        """Test creating a request via private API (with auth)."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=private.request.create&output=json",
            json=request_create_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.create(
            note="Test note",
            category_id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

        assert request.x_request == 12750
        assert request.accesskey == "12750abc123"

    def test_create_with_custom_fields(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_create_data: dict,
    ):
        """Test creating a request with custom fields."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=private.request.create&output=json",
            json=request_create_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.create(
            note="Test note",
            category_id=1,
            email="test@example.com",
            custom_fields={1: "Value 1", 2: "Value 2"},
        )

        assert request.x_request == 12750

    def test_create_urgent(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_create_data: dict,
    ):
        """Test creating an urgent request."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=private.request.create&output=json",
            json=request_create_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.create(
            note="Urgent issue",
            category_id=1,
            email="test@example.com",
            is_urgent=True,
        )

        assert request.x_request == 12750


class TestRequestsAPIGet:
    """Tests for RequestsAPI.get()."""

    def test_get_by_request_id(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_get_data: dict,
    ):
        """Test getting a request by ID (private API)."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.get&xRequest=12745&output=json",
            json=request_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.get(request_id=12745)

        assert request.x_request == 12745
        assert request.email == "john.doe@example.com"
        assert request.first_name == "John"
        assert request.last_name == "Doe"
        assert request.title == "RE: Information on Your Request"

    def test_get_by_access_key(
        self,
        base_url: str,
        httpx_mock,
        request_get_data: dict,
    ):
        """Test getting a request by access key (public API)."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=request.get&accesskey=12745itetxb&output=json",
            json=request_get_data,
        )

        client = HelpSpotClient(base_url=base_url)
        request = client.requests.get(access_key="12745itetxb")

        assert request.x_request == 12745
        assert request.accesskey == "12745itetxb"

    def test_get_with_raw_values(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_get_data: dict,
    ):
        """Test getting a request with raw values."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.get&xRequest=12745&fRawValues=1&output=json",
            json=request_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.get(request_id=12745, raw_values=True)

        assert request.x_request == 12745

    def test_get_without_id_or_key_raises_error(
        self,
        base_url: str,
        api_token: str,
    ):
        """Test that get() raises ValidationError if neither ID nor key provided."""
        client = HelpSpotClient(base_url=base_url, api_token=api_token)

        with pytest.raises(
            ValidationError, match="Either request_id or access_key must be provided"
        ):
            client.requests.get()


class TestRequestsAPIUpdate:
    """Tests for RequestsAPI.update()."""

    def test_update_by_request_id(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_get_data: dict,
    ):
        """Test updating a request by ID (private API)."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=private.request.update&output=json",
            json=request_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.update(
            request_id=12745,
            note="Update note",
            status_id=2,
        )

        assert request.x_request == 12745

    def test_update_by_access_key(
        self,
        base_url: str,
        httpx_mock,
        request_get_data: dict,
    ):
        """Test updating a request by access key (public API)."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=request.update&output=json",
            json=request_get_data,
        )

        client = HelpSpotClient(base_url=base_url)
        request = client.requests.update(
            access_key="12745itetxb",
            note="Update note",
        )

        assert request.x_request == 12745

    def test_update_with_multiple_fields(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_get_data: dict,
    ):
        """Test updating a request with multiple fields."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=private.request.update&output=json",
            json=request_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        request = client.requests.update(
            request_id=12745,
            note="Update note",
            category_id=2,
            assigned_to=5,
            status_id=3,
            is_open=False,
            is_urgent=True,
            title="Updated title",
        )

        assert request.x_request == 12745

    def test_update_without_id_or_key_raises_error(
        self,
        base_url: str,
        api_token: str,
    ):
        """Test that update() raises ValidationError if neither ID nor key provided."""
        client = HelpSpotClient(base_url=base_url, api_token=api_token)

        with pytest.raises(
            ValidationError, match="Either request_id or access_key must be provided"
        ):
            client.requests.update(note="Update note")


class TestRequestsAPISearch:
    """Tests for RequestsAPI.search()."""

    def test_search_basic(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_search_data: dict,
    ):
        """Test basic request search."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.search&start=0&length=50&orderByDir=desc&output=json",
            json=request_search_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.requests.search()

        assert len(requests) == 2
        assert requests[0].x_request == 12745
        assert requests[1].x_request == 12746

    def test_search_with_query(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_search_data: dict,
    ):
        """Test searching with a text query."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.search&start=0&length=50&orderByDir=desc&sSearch=printer&output=json",
            json=request_search_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.requests.search(query="printer")

        assert len(requests) == 2

    def test_search_with_filters(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_search_data: dict,
    ):
        """Test searching with various filters."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.search&start=0&length=50&orderByDir=desc&xCategory=1&fOpen=1&output=json",
            json=request_search_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.requests.search(
            category_id=1,
            is_open=True,
        )

        assert len(requests) == 2

    def test_search_with_pagination(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_search_data: dict,
    ):
        """Test searching with pagination."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.search&start=10&length=25&orderByDir=asc&output=json",
            json=request_search_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.requests.search(
            start=10,
            length=25,
            order_dir="asc",
        )

        assert len(requests) == 2

    def test_search_by_email(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        request_search_data: dict,
    ):
        """Test searching by customer email."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.search&start=0&length=50&orderByDir=desc&sEmail=john.doe%40example.com&output=json",
            json=request_search_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.requests.search(email="john.doe@example.com")

        assert len(requests) == 2


class TestRequestsAPIErrors:
    """Tests for error handling in RequestsAPI."""

    def test_api_error_handling(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        api_error_data: dict,
    ):
        """Test that API errors are properly handled."""
        httpx_mock.add_response(
            method="POST",
            url=f"{base_url}/api/index.php?method=private.request.create&output=json",
            json=api_error_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)

        with pytest.raises(APIError) as exc_info:
            client.requests.create(note="Test note", category_id=1)

        assert exc_info.value.error_id == 101
        assert "Required field missing" in str(exc_info.value)
