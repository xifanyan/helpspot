"""Status types API endpoints."""

from __future__ import annotations

from helpspot.api.base import BaseAPI
from helpspot.models import StatusType


class StatusTypesAPI(BaseAPI):
    """API methods for status type operations (private API only)."""

    def list(self, active_only: bool = True) -> list[StatusType]:
        """List all status types.

        Args:
            active_only: Return only active status types (default True).

        Returns:
            List of StatusType objects.

        Raises:
            AuthenticationRequiredError: If not authenticated.
        """
        params = {"fActiveOnly": "1" if active_only else "0"}

        result = self._request(
            "GET", "private.request.getStatusTypes", params=params, require_auth=True
        )

        # Handle response format
        status_data = result.get("results", {}).get("status", [])
        if isinstance(status_data, dict):
            status_data = [status_data]

        return [StatusType(**status) for status in status_data]
