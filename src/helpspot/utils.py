"""Utility functions for the HelpSpot API client."""

import base64
import logging
from typing import Any

logger = logging.getLogger("helpspot")


def encode_file_content(content: bytes) -> str:
    """Encode file content to base64 string.

    Args:
        content: The raw file content as bytes.

    Returns:
        Base64 encoded string.
    """
    return base64.b64encode(content).decode("utf-8")


def prepare_custom_fields(custom_fields: dict[int, str] | None) -> dict[str, str]:
    """Convert custom fields dict to API parameter format.

    Args:
        custom_fields: Dictionary mapping custom field ID to value.
            Example: {1: "value1", 2: "value2"}

    Returns:
        Dictionary with Custom# keys.
            Example: {"Custom1": "value1", "Custom2": "value2"}
    """
    if not custom_fields:
        return {}

    return {f"Custom{field_id}": value for field_id, value in custom_fields.items()}


def prepare_file_uploads(files: list[dict[str, Any]] | None) -> dict[str, str]:
    """Prepare file uploads for API request.

    Args:
        files: List of file dictionaries with keys:
            - filename: str
            - mime_type: str
            - content: bytes

    Returns:
        Dictionary with File#_* keys ready for API submission.
    """
    if not files:
        return {}

    result: dict[str, str] = {}
    for idx, file_info in enumerate(files, start=1):
        result[f"File{idx}_sFilename"] = file_info["filename"]
        result[f"File{idx}_sFileMimeType"] = file_info["mime_type"]
        result[f"File{idx}_bFileBody"] = encode_file_content(file_info["content"])

    return result


def validate_base_url(base_url: str) -> str:
    """Validate and normalize the base URL.

    Args:
        base_url: The base URL of the HelpSpot installation.

    Returns:
        Normalized base URL (without trailing slash).

    Raises:
        ValueError: If the URL is invalid.
    """
    if not base_url:
        raise ValueError("base_url cannot be empty")

    # Strip trailing slashes
    base_url = base_url.rstrip("/")

    # Validate URL scheme
    if not base_url.startswith(("http://", "https://")):
        raise ValueError("base_url must start with http:// or https://")

    return base_url
