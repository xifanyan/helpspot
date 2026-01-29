"""Exception classes for the HelpSpot API client."""


class HelpSpotError(Exception):
    """Base exception for all HelpSpot errors."""

    pass


class AuthenticationError(HelpSpotError):
    """Raised when authentication fails."""

    pass


class AuthenticationRequiredError(HelpSpotError):
    """Raised when a private API method is called without authentication."""

    pass


class APIError(HelpSpotError):
    """Raised when the API returns an error response."""

    def __init__(self, error_id: int, description: str) -> None:
        """Initialize API error.

        Args:
            error_id: The error ID from the API response.
            description: The error description from the API response.
        """
        self.error_id = error_id
        self.description = description
        super().__init__(f"API Error {error_id}: {description}")


class APIDisabledError(HelpSpotError):
    """Raised when the public or private API is not enabled on the server."""

    pass


class ValidationError(HelpSpotError):
    """Raised when request validation fails."""

    pass


class HTTPError(HelpSpotError):
    """Raised when an HTTP request fails."""

    pass
