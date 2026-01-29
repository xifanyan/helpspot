"""Customer API endpoints."""

from __future__ import annotations

from helpspot.api.base import BaseAPI
from helpspot.models import Request


class CustomersAPI(BaseAPI):
    """API methods for customer operations."""

    def get_requests(self, email: str, password: str) -> list[Request]:
        """Get all requests for a customer (public API).

        Args:
            email: Customer email address.
            password: Customer portal password.

        Returns:
            List of Request objects for the customer.

        Raises:
            APIError: If authentication fails or API returns error.
        """
        params = {"sEmail": email, "sPassword": password}

        result = self._request("GET", "customer.getRequests", params=params)

        # Handle both single request and array
        requests_data = result.get("requests", {}).get("request", [])
        if isinstance(requests_data, dict):
            requests_data = [requests_data]

        return [Request(**req) for req in requests_data]
