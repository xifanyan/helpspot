"""Status type data models."""

from __future__ import annotations

from pydantic import Field

from .common import HelpSpotBaseModel


class StatusType(HelpSpotBaseModel):
    """Represents a status type."""

    x_status: int = Field(alias="xStatus")
    name: str = Field(alias="sStatus")
