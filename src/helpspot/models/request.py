"""Request-related data models."""

from __future__ import annotations

from pydantic import Field, field_validator

from .common import HelpSpotBaseModel


class Request(HelpSpotBaseModel):
    """Represents a HelpSpot request/ticket."""

    x_request: int = Field(alias="xRequest")
    opened_via: str | None = Field(default=None, alias="fOpenedVia")
    opened_via_id: int | None = Field(default=None, alias="xOpenedViaId")
    person_opened_by: str | None = Field(default=None, alias="xPersonOpenedBy")
    person_assigned_to: str | None = Field(default=None, alias="xPersonAssignedTo")
    is_open: bool | None = Field(default=None, alias="fOpen")
    status: str | None = Field(default=None, alias="xStatus")
    is_urgent: bool | None = Field(default=None, alias="fUrgent")
    category: str | None = Field(default=None, alias="xCategory")
    opened_date: int | str | None = Field(default=None, alias="dtGMTOpened")
    closed_date: int | str | None = Field(default=None, alias="dtGMTClosed")
    request_password: str | None = Field(default=None, alias="sRequestPassword")
    title: str | None = Field(default=None, alias="sTitle")
    user_id: str | None = Field(default=None, alias="sUserId")
    first_name: str | None = Field(default=None, alias="sFirstName")
    last_name: str | None = Field(default=None, alias="sLastName")
    email: str | None = Field(default=None, alias="sEmail")
    phone: str | None = Field(default=None, alias="sPhone")
    last_reply_by: str | None = Field(default=None, alias="iLastReplyBy")
    is_trash: bool | None = Field(default=None, alias="fTrash")
    trashed_date: int | str | None = Field(default=None, alias="dtGMTTrashed")
    full_name: str | None = Field(default=None, alias="fullname")
    note: str | None = Field(default=None, alias="tNote")
    access_key: str | None = Field(default=None, alias="accesskey")

    @field_validator("opened_date", "closed_date", "trashed_date", mode="before")
    @classmethod
    def parse_date_field(cls, v: int | str | None) -> int | None:
        """Parse date fields - accept both timestamps and formatted strings."""
        if v is None or v == "":
            return None
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            # If it's a formatted date string, return None (we can't parse it without knowing format)
            # In production, you might want to parse these properly
            return None
        return None


class RequestHistory(HelpSpotBaseModel):
    """Represents a request history item."""

    x_request_history: int = Field(alias="xRequestHistory")
    x_request: int = Field(alias="xRequest")
    x_person: str | None = Field(default=None, alias="xPerson")
    change_date: str | None = Field(default=None, alias="dtGMTChange")
    is_public: bool = Field(alias="fPublic")
    is_initial: bool = Field(alias="fInitial")
    log: str | None = Field(default=None, alias="tLog")
    note: str | None = Field(default=None, alias="tNote")
    email_headers: str | None = Field(default=None, alias="tEmailHeaders")
    is_html: bool = Field(alias="fNoteIsHTML")
    is_merged: bool = Field(alias="fMergedFromRequest")


class RequestCreate(HelpSpotBaseModel):
    """Parameters for creating a request."""

    note: str
    category_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    user_id: str | None = None
    email: str | None = None
    phone: str | None = None
    is_urgent: bool = False
    custom_fields: dict[int, str] | None = None


class RequestUpdate(HelpSpotBaseModel):
    """Parameters for updating a request."""

    request_id: int | None = None
    access_key: str | None = None
    note: str | None = None
    category_id: int | None = None
    assigned_to: int | None = None
    status_id: int | None = None
    is_open: bool | None = None
    is_urgent: bool | None = None
