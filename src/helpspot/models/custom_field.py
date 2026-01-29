"""Custom field data models."""

from __future__ import annotations

from pydantic import Field

from .common import HelpSpotBaseModel


class CustomField(HelpSpotBaseModel):
    """Represents a custom field definition."""

    x_custom_field: int = Field(alias="xCustomField")
    field_name: str = Field(alias="fieldName")
    is_required: bool = Field(default=False, alias="isRequired")
    is_public: bool = Field(default=True, alias="isPublic")
    field_type: str = Field(alias="fieldType")
    order: int = Field(default=0, alias="iOrder")
    text_size: str | None = Field(default=None, alias="sTxtSize")
    large_text_rows: int | None = Field(default=None, alias="lrgTextRows")
    list_items: list[str] | None = Field(default=None, alias="listItems")
    decimal_places: int = Field(default=0, alias="iDecimalPlaces")
    regex: str | None = Field(default=None, alias="sRegex")
    ajax_url: str | None = Field(default=None, alias="sAjaxUrl")
    is_always_visible: bool = Field(default=False, alias="isAlwaysVisible")
