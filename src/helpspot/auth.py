"""Authentication handlers for HelpSpot API."""

from __future__ import annotations

from typing import Any

import httpx


class BearerAuth(httpx.Auth):
    """Bearer token authentication for API requests.

    This is the recommended authentication method for HelpSpot API.
    API tokens can be generated in staff preferences area.
    """

    def __init__(self, token: str) -> None:
        """Initialize Bearer token authentication.

        Args:
            token: The API token generated from HelpSpot staff preferences.
        """
        self.token = token

    def auth_flow(self, request: httpx.Request) -> Any:
        """Add Authorization header to the request.

        Args:
            request: The httpx request to authenticate.

        Yields:
            The response from the request.
        """
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


# BasicAuth is available directly from httpx.BasicAuth
# No need to create a custom class
