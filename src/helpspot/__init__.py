"""HelpSpot API Python client library.

This library provides a Python interface to the HelpSpot API for managing
support requests, customers, categories, and more.

Example:
    >>> from helpspot import HelpSpotClient
    >>> client = HelpSpotClient(
    ...     base_url="https://support.example.com",
    ...     api_token="your_token_here"
    ... )
    >>> request = client.requests.get(request_id=123)
    >>> print(request.title)
"""

from helpspot.client import HelpSpotClient
from helpspot.exceptions import (
    APIDisabledError,
    APIError,
    AuthenticationError,
    AuthenticationRequiredError,
    HelpSpotError,
    HTTPError,
    ValidationError,
)
from helpspot.models import (
    Category,
    Customer,
    CustomField,
    Filter,
    Request,
    RequestCreate,
    RequestHistory,
    RequestUpdate,
    StatusType,
    VersionInfo,
)

__version__ = "0.1.0"

__all__ = [
    "HelpSpotClient",
    # Exceptions
    "HelpSpotError",
    "AuthenticationError",
    "AuthenticationRequiredError",
    "APIError",
    "APIDisabledError",
    "ValidationError",
    "HTTPError",
    # Models
    "Request",
    "RequestHistory",
    "RequestCreate",
    "RequestUpdate",
    "Customer",
    "Category",
    "CustomField",
    "Filter",
    "StatusType",
    "VersionInfo",
]
