"""Tests for Categories, Customers, CustomFields, Filters, and StatusTypes APIs."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from helpspot import HelpSpotClient


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def categories_list_data(fixtures_dir: Path) -> dict:
    """Load categories.list fixture data."""
    with open(fixtures_dir / "categories_list.json") as f:
        return json.load(f)


@pytest.fixture
def filters_list_data(fixtures_dir: Path) -> dict:
    """Load filters.list fixture data."""
    with open(fixtures_dir / "filters_list.json") as f:
        return json.load(f)


@pytest.fixture
def filter_get_data(fixtures_dir: Path) -> dict:
    """Load filter.get fixture data."""
    with open(fixtures_dir / "filter_get.json") as f:
        return json.load(f)


@pytest.fixture
def custom_fields_list_data(fixtures_dir: Path) -> dict:
    """Load custom_fields.list fixture data."""
    with open(fixtures_dir / "custom_fields_list.json") as f:
        return json.load(f)


@pytest.fixture
def status_types_list_data(fixtures_dir: Path) -> dict:
    """Load status_types.list fixture data."""
    with open(fixtures_dir / "status_types_list.json") as f:
        return json.load(f)


@pytest.fixture
def customer_requests_data(fixtures_dir: Path) -> dict:
    """Load customer.getRequests fixture data."""
    with open(fixtures_dir / "customer_requests.json") as f:
        return json.load(f)


class TestCategoriesAPI:
    """Tests for CategoriesAPI."""

    def test_list_public_api(
        self,
        base_url: str,
        httpx_mock,
        categories_list_data: dict,
    ):
        """Test listing categories via public API."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=request.getCategories&output=json",
            json=categories_list_data,
        )

        client = HelpSpotClient(base_url=base_url)
        categories = client.categories.list()

        assert len(categories) == 3
        assert categories[0].x_category == 1
        assert categories[0].category == "Bugs"
        assert categories[1].x_category == 2
        assert categories[1].category == "Support"

    def test_list_private_api(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        categories_list_data: dict,
    ):
        """Test listing categories via private API."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.getCategories&output=json",
            json=categories_list_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        categories = client.categories.list()

        assert len(categories) == 3


class TestCustomersAPI:
    """Tests for CustomersAPI."""

    def test_get_requests(
        self,
        base_url: str,
        httpx_mock,
        customer_requests_data: dict,
    ):
        """Test getting customer requests."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=customer.getRequests&sEmail=john.doe%40example.com&sPassword=password123&output=json",
            json=customer_requests_data,
        )

        client = HelpSpotClient(base_url=base_url)
        requests = client.customers.get_requests(
            email="john.doe@example.com",
            password="password123",
        )

        assert len(requests) == 1
        assert requests[0].x_request == 12745
        assert requests[0].email == "john.doe@example.com"


class TestCustomFieldsAPI:
    """Tests for CustomFieldsAPI."""

    def test_list_all_fields(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        custom_fields_list_data: dict,
    ):
        """Test listing all custom fields."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.getCustomFields&output=json",
            json=custom_fields_list_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        fields = client.custom_fields.list()

        assert len(fields) == 3
        assert fields[0].field_id == 1
        assert fields[0].field_name == "Department"
        assert fields[0].field_type == "select"
        assert fields[0].is_required == 1

    def test_list_fields_by_category(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        custom_fields_list_data: dict,
    ):
        """Test listing custom fields filtered by category."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.getCustomFields&xCategory=1&output=json",
            json=custom_fields_list_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        fields = client.custom_fields.list(category_id=1)

        assert len(fields) == 3


class TestFiltersAPI:
    """Tests for FiltersAPI."""

    def test_list_filters(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        filters_list_data: dict,
    ):
        """Test listing filters."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.user.getFilters&output=json",
            json=filters_list_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        filters = client.filters.list()

        assert len(filters) == 2
        assert filters[0].x_filter == 1
        assert filters[0].filter_name == "My Open Requests"
        assert filters[1].x_filter == 42
        assert filters[1].filter_name == "Urgent Bugs"

    def test_get_filter_results(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        filter_get_data: dict,
    ):
        """Test getting filter results."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.filter.get&xFilter=42&start=0&length=50&output=json",
            json=filter_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.filters.get(filter_id="42")

        assert len(requests) == 1
        assert requests[0].x_request == 12746
        assert requests[0].urgent == 1

    def test_get_inbox_filter(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        filter_get_data: dict,
    ):
        """Test getting inbox filter results."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.filter.get&xFilter=inbox&start=0&length=50&output=json",
            json=filter_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.filters.get(filter_id="inbox")

        assert len(requests) == 1

    def test_get_filter_with_pagination(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        filter_get_data: dict,
    ):
        """Test getting filter results with pagination."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.filter.get&xFilter=42&start=20&length=10&output=json",
            json=filter_get_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        requests = client.filters.get(filter_id="42", start=20, length=10)

        assert len(requests) == 1


class TestStatusTypesAPI:
    """Tests for StatusTypesAPI."""

    def test_list_status_types(
        self,
        base_url: str,
        api_token: str,
        httpx_mock,
        status_types_list_data: dict,
    ):
        """Test listing status types."""
        httpx_mock.add_response(
            method="GET",
            url=f"{base_url}/api/index.php?method=private.request.getStatusTypes&output=json",
            json=status_types_list_data,
        )

        client = HelpSpotClient(base_url=base_url, api_token=api_token)
        statuses = client.status_types.list()

        assert len(statuses) == 3
        assert statuses[0].x_status == 1
        assert statuses[0].status == "Active"
        assert statuses[1].x_status == 2
        assert statuses[1].status == "Waiting on Customer"
        assert statuses[2].x_status == 3
        assert statuses[2].status == "Closed"
