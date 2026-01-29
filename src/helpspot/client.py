"""Main HelpSpot API client."""

from __future__ import annotations

import logging

import httpx

from helpspot.api import (
    CategoriesAPI,
    CustomersAPI,
    CustomFieldsAPI,
    FiltersAPI,
    RequestsAPI,
    StatusTypesAPI,
)
from helpspot.auth import BearerAuth
from helpspot.models import VersionInfo
from helpspot.utils import validate_base_url

logger = logging.getLogger("helpspot")


class HelpSpotClient:
    """Main client for interacting with the HelpSpot API.

    Example:
        >>> client = HelpSpotClient(
        ...     base_url="https://support.example.com",
        ...     api_token="your_token_here"
        ... )
        >>> request = client.requests.get(request_id=123)
        >>> print(request.title)
    """

    def __init__(
        self,
        base_url: str,
        api_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        output_format: str = "json",
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize the HelpSpot client.

        Args:
            base_url: Base URL of your HelpSpot installation
                (e.g., "https://support.example.com").
            api_token: API token from staff preferences (recommended).
            username: Username for basic auth (alternative to api_token).
            password: Password for basic auth (required if username provided).
            output_format: API output format ("json", "xml", or "php"). Default: "json".
            timeout: Request timeout in seconds. Default: 30.0.
            verify_ssl: Whether to verify SSL certificates. Set to False to bypass
                certificate verification (not recommended for production). Default: True.

        Raises:
            ValueError: If base_url is invalid or auth parameters are incomplete.

        Example:
            >>> # Using API token (recommended)
            >>> client = HelpSpotClient(
            ...     base_url="https://support.example.com",
            ...     api_token="1|5VdNXJEtsPoFpX1KH5yc0BO2wlCqDp0sRTxZtox3"
            ... )
            >>>
            >>> # Using basic authentication
            >>> client = HelpSpotClient(
            ...     base_url="https://support.example.com",
            ...     username="user@example.com",
            ...     password="password123"
            ... )
            >>>
            >>> # Bypass SSL verification (for self-signed certificates)
            >>> client = HelpSpotClient(
            ...     base_url="https://support.example.com",
            ...     api_token="your_token",
            ...     verify_ssl=False
            ... )
        """
        # Validate and normalize base URL
        self.base_url = validate_base_url(base_url)
        self.output_format = output_format

        # Set up authentication
        self.auth: httpx.Auth | None = None
        if api_token:
            self.auth = BearerAuth(api_token)
            logger.debug("Using Bearer token authentication")
        elif username and password:
            self.auth = httpx.BasicAuth(username, password)
            logger.debug("Using Basic authentication")
        elif username or password:
            raise ValueError("Both username and password must be provided for basic auth")
        else:
            logger.debug("No authentication provided (public API only)")

        # Create HTTP client
        self._http_client = httpx.Client(auth=self.auth, timeout=timeout, verify=verify_ssl)

        if not verify_ssl:
            logger.warning(
                "SSL certificate verification is disabled. "
                "This is not recommended for production use."
            )

        # Initialize API endpoints
        self.requests = RequestsAPI(self)
        self.customers = CustomersAPI(self)
        self.categories = CategoriesAPI(self)
        self.custom_fields = CustomFieldsAPI(self)
        self.filters = FiltersAPI(self)
        self.status_types = StatusTypesAPI(self)

        logger.info(f"HelpSpot client initialized for {self.base_url}")

    def version(self) -> VersionInfo:
        """Get API version information.

        Returns:
            VersionInfo with version and min_version.

        Example:
            >>> client = HelpSpotClient(base_url="https://support.example.com")
            >>> version = client.version()
            >>> print(f"API version: {version.version}")
        """
        url = f"{self.base_url}/api/index.php"
        params = {"method": "version", "output": self.output_format}

        response = self._http_client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        return VersionInfo(**result)

    def close(self) -> None:
        """Close the HTTP client and clean up resources.

        It's recommended to use the client as a context manager instead.

        Example:
            >>> client = HelpSpotClient(base_url="...")
            >>> try:
            ...     # Use client
            ...     pass
            ... finally:
            ...     client.close()
        """
        self._http_client.close()

    def __enter__(self) -> HelpSpotClient:
        """Context manager entry."""
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.close()
