"""Filter-related data models."""

from __future__ import annotations

from pydantic import Field

from .common import HelpSpotBaseModel


class Filter(HelpSpotBaseModel):
    """Represents a request filter."""

    x_filter: str = Field(alias="xFilter")
    name: str = Field(alias="sFilterName")
    is_global: bool = Field(default=False, alias="fGlobal")
    folder: str | None = Field(default=None, alias="sFilterFolder")
    count: int | None = Field(default=None, alias="count")
    unread: int | None = Field(default=None, alias="unread")
