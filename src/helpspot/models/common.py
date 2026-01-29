"""Common models and base classes."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class HelpSpotBaseModel(BaseModel):
    """Base model for all HelpSpot data models.

    Configured to allow population by field name or alias.
    """

    model_config = ConfigDict(populate_by_name=True)


class FileAttachment(HelpSpotBaseModel):
    """Represents a file attachment."""

    filename: str
    mime_type: str
    content: bytes
