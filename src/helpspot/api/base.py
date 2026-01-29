"""Base API class with common functionality."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import httpx

from helpspot.exceptions import (
    APIDisabledError,
    APIError,
    AuthenticationRequiredError,
    HTTPError,
)

if TYPE_CHECKING:
    from helpspot.client import HelpSpotClient

logger = logging.getLogger("helpspot")


class BaseAPI:
    """Base class for all API endpoint classes."""

    def __init__(self, client: HelpSpotClient) -> None:
        """Initialize the API with a client reference.

        Args:
            client: The HelpSpotClient instance.
        """
        self.client = client

    def _request(
        self,
        method: str,
        api_method: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        require_auth: bool = False,
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: HTTP method (GET or POST).
            api_method: HelpSpot API method name (e.g., 'request.get').
            params: Query parameters.
            data: Form data for POST requests.
            require_auth: Whether authentication is required.

        Returns:
            Parsed JSON response.

        Raises:
            AuthenticationRequiredError: If auth required but not provided.
            APIError: If the API returns an error.
            APIDisabledError: If the API is not enabled.
            HTTPError: If the HTTP request fails.
        """
        if require_auth and not self.client.auth:
            raise AuthenticationRequiredError(
                f"Authentication required for method '{api_method}'. "
                "Please provide api_token or username/password."
            )

        # Build URL
        url = f"{self.client.base_url}/api/index.php"

        # Build parameters
        request_params = {"method": api_method, "output": self.client.output_format}
        if params:
            request_params.update(params)

        logger.debug(f"Making {method} request to {api_method}")

        try:
            if method.upper() == "GET":
                response = self.client._http_client.get(url, params=request_params)
            elif method.upper() == "POST":
                response = self.client._http_client.post(url, params=request_params, data=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise HTTPError(f"HTTP request failed: {e}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise HTTPError(f"Request failed: {e}") from e

        # Parse response
        try:
            result = response.json()
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise HTTPError(f"Invalid JSON response: {e}") from e

        # Check for API errors
        if "errors" in result:
            errors = result["errors"]
            if isinstance(errors, dict) and "error" in errors:
                error = errors["error"]
                if isinstance(error, list):
                    error = error[0]
                error_id = error.get("id", 0)
                description = error.get("description", "Unknown error")
                raise APIError(error_id, description)

        if "reply" in result and "not enabled" in str(result["reply"]).lower():
            raise APIDisabledError(result["reply"])

        return result
