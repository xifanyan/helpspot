"""Request API endpoints."""

from __future__ import annotations

from typing import Any

from helpspot.api.base import BaseAPI
from helpspot.models import Request
from helpspot.utils import prepare_custom_fields, prepare_file_uploads


class RequestsAPI(BaseAPI):
    """API methods for managing requests."""

    def create(
        self,
        note: str,
        category_id: int | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        user_id: str | None = None,
        phone: str | None = None,
        title: str | None = None,
        is_urgent: bool = False,
        portal_id: int | None = None,
        custom_fields: dict[int, str] | None = None,
        files: list[dict[str, Any]] | None = None,
    ) -> Request:
        """Create a new request.

        Works as public API if no auth, or private API if authenticated.
        At least one of email, first_name, last_name, user_id, or phone must be provided.

        Args:
            note: The request note/description (required).
            category_id: Category ID (required for private API).
            email: Customer email address.
            first_name: Customer first name.
            last_name: Customer last name.
            user_id: Customer ID.
            phone: Customer phone number.
            title: Request title/subject.
            is_urgent: Mark request as urgent.
            portal_id: Portal ID.
            custom_fields: Dict mapping custom field ID to value.
            files: List of file dicts with 'filename', 'mime_type', 'content' keys.

        Returns:
            Created Request object with xRequest and accesskey.

        Raises:
            ValidationError: If required fields are missing.
            APIError: If the API returns an error.
        """
        data: dict[str, Any] = {"tNote": note}

        if category_id is not None:
            data["xCategory"] = str(category_id)
        if email:
            data["sEmail"] = email
        if first_name:
            data["sFirstName"] = first_name
        if last_name:
            data["sLastName"] = last_name
        if user_id:
            data["sUserId"] = user_id
        if phone:
            data["sPhone"] = phone
        if title:
            data["sTitle"] = title
        if is_urgent:
            data["fUrgent"] = "1"
        if portal_id is not None:
            data["xPortal"] = str(portal_id)

        # Add custom fields
        if custom_fields:
            data.update(prepare_custom_fields(custom_fields))

        # Add file uploads
        if files:
            data.update(prepare_file_uploads(files))

        # Determine if using private or public API
        method = "private.request.create" if self.client.auth else "request.create"
        require_auth = self.client.auth is not None

        result = self._request("POST", method, data=data, require_auth=require_auth)

        # The create endpoint returns just the xRequest ID directly, not wrapped in "request"
        # Response format: {"xRequest": "123456"}
        if "request" in result:
            return Request(**result["request"])
        else:
            # Direct response - create minimal Request object with just the ID
            return Request(xRequest=int(result.get("xRequest", 0)))

    def get(
        self,
        request_id: int | None = None,
        access_key: str | None = None,
        raw_values: bool = False,
    ) -> Request:
        """Get request details.

        Use access_key for public API, or request_id for private API.

        Args:
            request_id: Request ID (for private API with auth).
            access_key: Access key (for public API without auth).
            raw_values: Return raw numeric values instead of text.

        Returns:
            Request object with full details.

        Raises:
            ValidationError: If neither request_id nor access_key provided.
            APIError: If the API returns an error.
        """
        params: dict[str, Any] = {}

        if access_key:
            # Public API
            params["accesskey"] = access_key
            method = "request.get"
            require_auth = False
        elif request_id is not None:
            # Private API
            params["xRequest"] = str(request_id)
            if raw_values:
                params["fRawValues"] = "1"
            method = "private.request.get"
            require_auth = True
        else:
            from helpspot.exceptions import ValidationError

            raise ValidationError("Either request_id or access_key must be provided")

        result = self._request("GET", method, params=params, require_auth=require_auth)

        # Check if response is wrapped in "request" key or is direct
        if "request" in result:
            return Request(**result["request"])
        else:
            # Direct response format
            return Request(**result)

    def update(
        self,
        note: str,
        request_id: int | None = None,
        access_key: str | None = None,
        category_id: int | None = None,
        assigned_to: int | None = None,
        status_id: int | None = None,
        is_open: bool | None = None,
        is_urgent: bool | None = None,
        title: str | None = None,
        custom_fields: dict[int, str] | None = None,
        files: list[dict[str, Any]] | None = None,
    ) -> Request:
        """Update an existing request.

        Use access_key for public API, or request_id for private API.

        Args:
            note: Note to add to the request.
            request_id: Request ID (for private API).
            access_key: Access key (for public API).
            category_id: New category ID.
            assigned_to: Staff ID to assign to.
            status_id: New status ID.
            is_open: Open/close the request.
            is_urgent: Mark as urgent.
            title: Update title.
            custom_fields: Custom field values.
            files: File attachments.

        Returns:
            Updated Request object.

        Raises:
            ValidationError: If neither request_id nor access_key provided.
        """
        data: dict[str, Any] = {"tNote": note}

        if access_key:
            # Public API
            data["accesskey"] = access_key
            method = "request.update"
            require_auth = False
        elif request_id is not None:
            # Private API
            data["xRequest"] = str(request_id)
            method = "private.request.update"
            require_auth = True
        else:
            from helpspot.exceptions import ValidationError

            raise ValidationError("Either request_id or access_key must be provided")

        # Add optional fields
        if category_id is not None:
            data["xCategory"] = str(category_id)
        if assigned_to is not None:
            data["xPersonAssignedTo"] = str(assigned_to)
        if status_id is not None:
            data["xStatus"] = str(status_id)
        if is_open is not None:
            data["fOpen"] = "1" if is_open else "0"
        if is_urgent is not None:
            data["fUrgent"] = "1" if is_urgent else "0"
        if title:
            data["sTitle"] = title

        # Add custom fields
        if custom_fields:
            data.update(prepare_custom_fields(custom_fields))

        # Add file uploads
        if files:
            data.update(prepare_file_uploads(files))

        result = self._request("POST", method, data=data, require_auth=require_auth)

        # Check if response is wrapped or direct
        if "request" in result:
            return Request(**result["request"])
        else:
            return Request(**result)

    def search(
        self,
        query: str | None = None,
        request_id: int | None = None,
        user_id: str | None = None,
        email: str | None = None,
        status_id: int | None = None,
        category_id: int | None = None,
        is_open: bool | None = None,
        assigned_to: int | None = None,
        start: int = 0,
        length: int = 50,
        order_by: str | None = None,
        order_dir: str = "desc",
        raw_values: bool = False,
    ) -> list[Request]:
        """Search for requests (private API only).

        Args:
            query: Full text search query.
            request_id: Filter by request ID.
            user_id: Filter by customer user ID.
            email: Filter by customer email.
            status_id: Filter by status.
            category_id: Filter by category.
            is_open: Filter by open/closed status.
            assigned_to: Filter by assigned staff ID.
            start: Starting position for pagination.
            length: Number of results to return.
            order_by: Field to order by.
            order_dir: Order direction ('asc' or 'desc').
            raw_values: Return raw numeric values.

        Returns:
            List of Request objects.

        Raises:
            AuthenticationRequiredError: If not authenticated.
        """
        params: dict[str, Any] = {
            "start": str(start),
            "length": str(length),
            "orderByDir": order_dir,
        }

        if query:
            params["sSearch"] = query
        if request_id is not None:
            params["xRequest"] = str(request_id)
        if user_id:
            params["sUserId"] = user_id
        if email:
            params["sEmail"] = email
        if status_id is not None:
            params["xStatus"] = str(status_id)
        if category_id is not None:
            params["xCategory"] = str(category_id)
        if is_open is not None:
            params["fOpen"] = "1" if is_open else "0"
        if assigned_to is not None:
            params["xPersonAssignedTo"] = str(assigned_to)
        if order_by:
            params["orderBy"] = order_by
        if raw_values:
            params["fRawValues"] = "1"

        result = self._request("GET", "private.request.search", params=params, require_auth=True)

        # Handle both single request and array of requests
        requests_data = result.get("requests", {}).get("request", [])
        if isinstance(requests_data, dict):
            requests_data = [requests_data]

        return [Request(**req) for req in requests_data]
