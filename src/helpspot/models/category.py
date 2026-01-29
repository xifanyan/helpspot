"""Category-related data models."""

from __future__ import annotations

from pydantic import Field, field_validator

from .common import HelpSpotBaseModel


class Category(HelpSpotBaseModel):
    """Represents a request category."""

    x_category: int = Field(alias="xCategory")
    name: str = Field(alias="sCategory")
    group: str | None = Field(default=None, alias="sCategoryGroup")
    is_deleted: bool = Field(default=False, alias="fDeleted")
    allow_public_submit: bool = Field(default=True, alias="fAllowPublicSubmit")
    default_person: int | str | None = Field(default=None, alias="xPersonDefault")
    auto_assign: int | bool = Field(default=False, alias="fAutoAssignTo")

    @field_validator("default_person", mode="before")
    @classmethod
    def parse_person_id(cls, v: int | str | None) -> int | None:
        """Parse person ID - convert empty string or '0' to None."""
        if v is None or v == "" or v == "0" or v == 0:
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return None
        return v

    @field_validator("auto_assign", mode="before")
    @classmethod
    def parse_auto_assign(cls, v: int | str | bool) -> int:
        """Parse auto_assign - can be 0, 1, or other numbers for different modes."""
        if isinstance(v, bool):
            return 1 if v else 0
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return 0
        return int(v) if v else 0
