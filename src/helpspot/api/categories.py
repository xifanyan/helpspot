"""Category API endpoints."""

from __future__ import annotations

from helpspot.api.base import BaseAPI
from helpspot.models import Category


class CategoriesAPI(BaseAPI):
    """API methods for category operations."""

    def list(self) -> list[Category]:
        """List all categories.

        Works for both public and private API depending on authentication.

        Returns:
            List of Category objects.

        Raises:
            APIError: If the API returns an error.
        """
        method = "private.request.getCategories" if self.client.auth else "request.getCategories"
        require_auth = self.client.auth is not None

        result = self._request("GET", method, require_auth=require_auth)

        # Handle response format
        # The API returns {"category": {"43": {...}, "35": {...}, ...}}
        categories_dict = result.get("category", {})

        # If empty or not a dict, try alternative format
        if not categories_dict:
            categories_data = result.get("categories", {}).get("category", [])
            if isinstance(categories_data, dict):
                categories_data = [categories_data]
            return [Category(**cat) for cat in categories_data]

        # Convert dict of categories (keyed by ID) to list
        if isinstance(categories_dict, dict):
            categories_list = list(categories_dict.values())
        else:
            categories_list = [categories_dict] if categories_dict else []

        return [Category(**cat) for cat in categories_list]
