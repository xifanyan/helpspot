"""Customer-related data models."""

from __future__ import annotations

from pydantic import Field

from .common import HelpSpotBaseModel


class Customer(HelpSpotBaseModel):
    """Represents a customer."""

    user_id: str | None = Field(default=None, alias="sUserId")
    first_name: str | None = Field(default=None, alias="sFirstName")
    last_name: str | None = Field(default=None, alias="sLastName")
    email: str | None = Field(default=None, alias="sEmail")
    phone: str | None = Field(default=None, alias="sPhone")
    full_name: str | None = Field(default=None, alias="fullname")
