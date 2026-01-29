"""Custom fields API endpoints."""

from __future__ import annotations

from helpspot.api.base import BaseAPI
from helpspot.models import CustomField


class CustomFieldsAPI(BaseAPI):
    """API methods for custom field operations."""

    def list(self, category_id: int | None = None) -> list[CustomField]:
        """List all custom fields.

        Works for both public and private API depending on authentication.

        Args:
            category_id: Optional category ID to filter fields (private API only).

        Returns:
            List of CustomField objects.

        Raises:
            APIError: If the API returns an error.
        """
        params = {}
        if category_id is not None:
            params["xCategory"] = str(category_id)

        method = (
            "private.request.getCustomFields" if self.client.auth else "request.getCustomFields"
        )
        require_auth = self.client.auth is not None

        result = self._request("GET", method, params=params, require_auth=require_auth)

        # Handle response format
        fields_data = result.get("customfields", {}).get("field", [])
        if isinstance(fields_data, dict):
            fields_data = [fields_data]

        return [CustomField(**field) for field in fields_data]
