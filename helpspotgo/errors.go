package helpspotgo

import (
	"encoding/json"
	"fmt"
)

var (
	ErrMissingBaseURL  = fmt.Errorf("missing base URL")
	ErrMissingAPIKey   = fmt.Errorf("missing API key")
	ErrMissingAuth     = fmt.Errorf("authentication required (use API key or username/password)")
	ErrInvalidResponse = fmt.Errorf("invalid response from server")
	ErrAPINotEnabled   = fmt.Errorf("API is not enabled on the server")
	ErrAuthentication  = fmt.Errorf("authentication failed")
	ErrNotFound        = fmt.Errorf("resource not found")
	ErrServerError     = fmt.Errorf("server error")
)

type APIError struct {
	Code        int    `json:"code"`
	Description string `json:"description"`
	StatusCode  int
}

func (e *APIError) Error() string {
	if e.Description != "" {
		return fmt.Sprintf("API Error %d: %s", e.Code, e.Description)
	}
	return fmt.Sprintf("API Error: HTTP %d", e.StatusCode)
}

func (c *Client) parseError(body []byte, statusCode int) error {
	var errResp ErrorResponse
	if err := json.Unmarshal(body, &errResp); err == nil {
		if len(errResp.Errors) > 0 {
			return &APIError{
				Code:        errResp.Errors[0].ID,
				Description: errResp.Errors[0].Description,
				StatusCode:  statusCode,
			}
		}
	}

	if statusCode == 400 {
		return &APIError{Code: 2, Description: "Bad Request", StatusCode: statusCode}
	}
	if statusCode == 401 {
		return &APIError{Code: 2, Description: "Authentication failed", StatusCode: statusCode}
	}
	if statusCode == 403 {
		return &APIError{Code: 3, Description: "Forbidden", StatusCode: statusCode}
	}
	if statusCode == 404 {
		return &APIError{Code: 4, Description: "Not Found", StatusCode: statusCode}
	}

	return &APIError{StatusCode: statusCode, Description: "Server error"}
}
