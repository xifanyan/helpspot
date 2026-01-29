"""API version information models."""

from __future__ import annotations

from pydantic import Field

from .common import HelpSpotBaseModel


class VersionInfo(HelpSpotBaseModel):
    """Represents API version information."""

    version: str = Field(alias="version")
    min_version: str = Field(alias="min_version")
