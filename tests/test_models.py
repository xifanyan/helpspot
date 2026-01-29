"""Tests for Pydantic models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from helpspot.models import (
    Category,
    CustomField,
    Customer,
    FileAttachment,
    Filter,
    Request,
    StatusType,
    VersionInfo,
)


class TestRequestModel:
    """Tests for Request model."""

    def test_create_request_basic(self):
        """Test creating a basic Request object."""
        request = Request(
            xRequest=12345,
            sEmail="test@example.com",
            sFirstName="John",
            sLastName="Doe",
        )

        assert request.x_request == 12345
        assert request.email == "test@example.com"
        assert request.first_name == "John"
        assert request.last_name == "Doe"

    def test_request_field_aliases(self):
        """Test that field aliases work correctly."""
        # Create with API field names (xRequest, sEmail, etc.)
        request = Request(
            xRequest=12345,
            sEmail="test@example.com",
            sFirstName="John",
            sLastName="Doe",
            fOpen=1,
            fUrgent=0,
        )

        # Access via Python names (x_request, email, etc.)
        assert request.x_request == 12345
        assert request.email == "test@example.com"
        assert request.open == 1
        assert request.urgent == 0

    def test_request_optional_fields(self):
        """Test Request with optional fields."""
        request = Request(
            xRequest=12345,
            sEmail="test@example.com",
            sTitle="Test Request",
            tNote="This is a test note",
            xStatus="Active",
            xCategory="Bugs",
        )

        assert request.title == "Test Request"
        assert request.note == "This is a test note"
        assert request.status == "Active"
        assert request.category == "Bugs"

    def test_request_populate_by_name(self):
        """Test that populate_by_name works (can use either alias or field name)."""
        # Should work with both naming conventions
        request1 = Request(xRequest=12345, sEmail="test@example.com")
        request2 = Request(x_request=12345, email="test@example.com")

        assert request1.x_request == request2.x_request
        assert request1.email == request2.email

    def test_request_timestamps(self):
        """Test Request with timestamp fields."""
        request = Request(
            xRequest=12345,
            sEmail="test@example.com",
            dtGMTOpened=1190598240,
            dtGMTClosed=1190699999,
        )

        assert request.gmt_opened == 1190598240
        assert request.gmt_closed == 1190699999

    def test_request_access_key(self):
        """Test Request with accesskey."""
        request = Request(
            xRequest=12345,
            sEmail="test@example.com",
            accesskey="12345abc123",
        )

        assert request.accesskey == "12345abc123"


class TestCategoryModel:
    """Tests for Category model."""

    def test_create_category(self):
        """Test creating a Category object."""
        category = Category(
            xCategory=1,
            sCategory="Bugs",
            sPersonalizedCatName="Bug Reports",
            fDeleted=0,
        )

        assert category.x_category == 1
        assert category.category == "Bugs"
        assert category.personalized_cat_name == "Bug Reports"
        assert category.deleted == 0

    def test_category_minimal(self):
        """Test creating a minimal Category object."""
        category = Category(xCategory=1, sCategory="Support")

        assert category.x_category == 1
        assert category.category == "Support"
        assert category.personalized_cat_name is None
        assert category.deleted is None


class TestCustomerModel:
    """Tests for Customer model."""

    def test_create_customer(self):
        """Test creating a Customer object."""
        customer = Customer(
            sEmail="customer@example.com",
            sFirstName="Jane",
            sLastName="Smith",
            sUserId="USER123",
            sPhone="555-1234",
        )

        assert customer.email == "customer@example.com"
        assert customer.first_name == "Jane"
        assert customer.last_name == "Smith"
        assert customer.user_id == "USER123"
        assert customer.phone == "555-1234"

    def test_customer_minimal(self):
        """Test creating a minimal Customer (email only)."""
        customer = Customer(sEmail="customer@example.com")

        assert customer.email == "customer@example.com"
        assert customer.first_name is None


class TestCustomFieldModel:
    """Tests for CustomField model."""

    def test_create_custom_field(self):
        """Test creating a CustomField object."""
        field = CustomField(
            fieldID=1,
            fieldName="Department",
            fieldType="select",
            isRequired=1,
            isPublic=1,
            isCategorySpecific=0,
            listItems="Sales,Support,Engineering",
        )

        assert field.field_id == 1
        assert field.field_name == "Department"
        assert field.field_type == "select"
        assert field.is_required == 1
        assert field.list_items == "Sales,Support,Engineering"

    def test_custom_field_category_specific(self):
        """Test CustomField with category restrictions."""
        field = CustomField(
            fieldID=2,
            fieldName="Priority",
            fieldType="select",
            isCategorySpecific=1,
            sCategoryList="1,2,3",
        )

        assert field.is_category_specific == 1
        assert field.category_list == "1,2,3"


class TestFilterModel:
    """Tests for Filter model."""

    def test_create_filter(self):
        """Test creating a Filter object."""
        filter_obj = Filter(
            xFilter=42,
            sFilterName="My Custom Filter",
            sFilterView="custom",
            tFilterDef='{"fUrgent":"1"}',
        )

        assert filter_obj.x_filter == 42
        assert filter_obj.filter_name == "My Custom Filter"
        assert filter_obj.filter_view == "custom"
        assert '{"fUrgent":"1"}' in filter_obj.filter_def

    def test_filter_inbox(self):
        """Test creating an inbox filter."""
        filter_obj = Filter(
            xFilter=1,
            sFilterName="Inbox",
            sFilterView="inbox",
        )

        assert filter_obj.filter_view == "inbox"


class TestStatusTypeModel:
    """Tests for StatusType model."""

    def test_create_status_type(self):
        """Test creating a StatusType object."""
        status = StatusType(
            xStatus=1,
            sStatus="Active",
            fOrder=1,
            fDeleted=0,
        )

        assert status.x_status == 1
        assert status.status == "Active"
        assert status.order == 1
        assert status.deleted == 0


class TestVersionInfoModel:
    """Tests for VersionInfo model."""

    def test_create_version_info(self):
        """Test creating a VersionInfo object."""
        version = VersionInfo(version="5.0", min_version="4.0")

        assert version.version == "5.0"
        assert version.min_version == "4.0"

    def test_version_info_optional_min(self):
        """Test VersionInfo with optional min_version."""
        version = VersionInfo(version="5.0")

        assert version.version == "5.0"
        assert version.min_version is None


class TestFileAttachmentModel:
    """Tests for FileAttachment model."""

    def test_create_file_attachment(self):
        """Test creating a FileAttachment object."""
        file_att = FileAttachment(
            filename="document.pdf",
            mime_type="application/pdf",
            content="base64encodedcontent",
        )

        assert file_att.filename == "document.pdf"
        assert file_att.mime_type == "application/pdf"
        assert file_att.content == "base64encodedcontent"

    def test_file_attachment_validation(self):
        """Test that FileAttachment requires all fields."""
        with pytest.raises(ValidationError):
            FileAttachment(filename="document.pdf")  # Missing required fields


class TestModelValidation:
    """Tests for model validation."""

    def test_request_missing_required_fields(self):
        """Test that Request validation fails without required fields."""
        # Request requires at least xRequest
        with pytest.raises(ValidationError):
            Request()

    def test_invalid_field_types(self):
        """Test that invalid field types raise validation errors."""
        with pytest.raises(ValidationError):
            Request(xRequest="not_an_int", sEmail="test@example.com")

    def test_extra_fields_allowed(self):
        """Test that extra fields are allowed (API may return unexpected fields)."""
        # Should not raise error with extra fields
        request = Request(
            xRequest=12345,
            sEmail="test@example.com",
            extra_field="some_value",
        )

        assert request.x_request == 12345
