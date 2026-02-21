package helpspotgo

import (
	"context"
	"encoding/json"
	"fmt"
)

func (c *Client) CreatePrivateRequest(ctx context.Context, params map[string]string) (*Request, error) {
	if params["tNote"] == "" {
		return nil, fmt.Errorf("tNote is required")
	}
	if params["xCategory"] == "" {
		return nil, fmt.Errorf("xCategory is required")
	}

	hasContact := params["sFirstName"] != "" || params["sLastName"] != "" ||
		params["sEmail"] != "" || params["sPhone"] != "" || params["sUserId"] != ""

	if !hasContact {
		return nil, fmt.Errorf("at least one of sFirstName, sLastName, sEmail, sPhone, or sUserId is required")
	}

	resp, err := c.Do(ctx, "private.request.create", params)
	if err != nil {
		return nil, err
	}
	return &resp.Request, nil
}

func (c *Client) GetPrivateRequest(ctx context.Context, requestID int) (*Request, error) {
	data, err := c.DoRaw(ctx, "private.request.get", map[string]string{"xRequest": fmt.Sprint(requestID)})
	if err != nil {
		return nil, err
	}

	var result Request
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil, fmt.Errorf("failed to parse request: %w", err)
	}

	return &result, nil
}

func (c *Client) UpdatePrivateRequest(ctx context.Context, params map[string]string) (*Request, error) {
	if params["xRequest"] == "" {
		return nil, fmt.Errorf("xRequest is required")
	}

	resp, err := c.Do(ctx, "private.request.update", params)
	if err != nil {
		return nil, err
	}
	return &resp.Request, nil
}

func (c *Client) GetMultipleRequests(ctx context.Context, requestIDs []int) ([]Request, error) {
	if len(requestIDs) == 0 {
		return nil, fmt.Errorf("at least one request ID is required")
	}

	params := make(map[string]string)
	for i, id := range requestIDs {
		params[fmt.Sprintf("xRequest[%d]", i)] = fmt.Sprint(id)
	}

	resp, err := c.Do(ctx, "private.request.multiGet", params)
	if err != nil {
		return nil, err
	}
	return resp.Requests, nil
}

func (c *Client) SearchPrivateRequests(ctx context.Context, params map[string]string) ([]Request, error) {
	data, err := c.DoRaw(ctx, "private.request.search", params)
	if err != nil {
		return nil, err
	}

	var result RequestsResponse
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		truncated := data
		if len(truncated) > 200 {
			truncated = truncated[:200] + "..."
		}
		return nil, fmt.Errorf("failed to parse requests: %w. Response: %s", err, truncated)
	}

	return result.Requests, nil
}

func (c *Client) GetPrivateCategories(ctx context.Context) ([]Category, error) {
	resp, err := c.Do(ctx, "private.request.getCategories", nil)
	if err != nil {
		return nil, err
	}
	return resp.Categories, nil
}

func (c *Client) GetPrivateCustomFields(ctx context.Context) ([]CustomField, error) {
	resp, err := c.Do(ctx, "private.request.getCustomFields", nil)
	if err != nil {
		return nil, err
	}
	return resp.CustomFields, nil
}

func (c *Client) GetMailboxes(ctx context.Context) ([]Mailbox, error) {
	resp, err := c.Do(ctx, "private.request.getMailboxes", nil)
	if err != nil {
		return nil, err
	}
	return resp.Mailboxes, nil
}

func (c *Client) GetStatusTypes(ctx context.Context) ([]StatusType, error) {
	resp, err := c.Do(ctx, "private.request.getStatusTypes", nil)
	if err != nil {
		return nil, err
	}
	return resp.StatusTypes, nil
}

func (c *Client) MarkRequestTrash(ctx context.Context, requestID int) error {
	_, err := c.Do(ctx, "private.request.markTrash", map[string]string{"xRequest": fmt.Sprint(requestID)})
	return err
}

func (c *Client) MarkRequestSpam(ctx context.Context, requestID int) error {
	_, err := c.Do(ctx, "private.request.markSpam", map[string]string{"xRequest": fmt.Sprint(requestID)})
	return err
}

func (c *Client) MergeRequests(ctx context.Context, primaryID, secondaryID int) error {
	params := map[string]string{
		"xRequest":  fmt.Sprint(primaryID),
		"xRequest2": fmt.Sprint(secondaryID),
	}
	_, err := c.Do(ctx, "private.request.merge", params)
	return err
}
