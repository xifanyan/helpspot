"""Filter API endpoints."""

from __future__ import annotations

from typing import Any

from helpspot.api.base import BaseAPI
from helpspot.models import Filter, Request


class FiltersAPI(BaseAPI):
    """API methods for filter operations (private API only)."""

    def list(self) -> list[Filter]:
        """List all filters for the authenticated user.

        Returns:
            List of Filter objects.

        Raises:
            AuthenticationRequiredError: If not authenticated.
        """
        result = self._request("GET", "private.user.getFilters", require_auth=True)

        # Handle response format
        filters_data = result.get("filters", {}).get("filter", [])
        if isinstance(filters_data, dict):
            filters_data = [filters_data]

        return [Filter(**f) for f in filters_data]

    def get(
        self,
        filter_id: str,
        start: int = 0,
        length: int = 50,
        raw_values: bool = False,
    ) -> list[Request]:
        """Get results from a filter.

        Args:
            filter_id: Filter ID (can be 'inbox', 'myq', or numeric ID).
            start: Starting position for pagination.
            length: Number of results to return.
            raw_values: Return raw numeric values.

        Returns:
            List of Request objects matching the filter.

        Raises:
            AuthenticationRequiredError: If not authenticated.
        """
        params: dict[str, Any] = {
            "xFilter": filter_id,
            "start": str(start),
            "length": str(length),
        }

        if raw_values:
            params["fRawValues"] = "1"

        result = self._request("GET", "private.filter.get", params=params, require_auth=True)

        # Handle response format
        requests_data = result.get("filter", {}).get("request", [])
        if isinstance(requests_data, dict):
            requests_data = [requests_data]

        return [Request(**req) for req in requests_data]
