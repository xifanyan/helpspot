package helpspotgo

import (
	"context"
	"encoding/json"
	"fmt"
)

func (c *Client) CreateRequest(ctx context.Context, params map[string]string) (*Request, error) {
	if params["tNote"] == "" {
		return nil, fmt.Errorf("tNote is required")
	}

	hasContact := params["sFirstName"] != "" || params["sLastName"] != "" ||
		params["sEmail"] != "" || params["sPhone"] != "" || params["sUserId"] != ""

	if !hasContact {
		return nil, fmt.Errorf("at least one of sFirstName, sLastName, sEmail, sPhone, or sUserId is required")
	}

	data, err := c.DoRaw(ctx, "request.create", params)
	if err != nil {
		return nil, err
	}

	var result Request
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil, fmt.Errorf("failed to parse request: %w", err)
	}

	return &result, nil
}

func (c *Client) GetRequest(ctx context.Context, accessKey string) (*Request, error) {
	data, err := c.DoRaw(ctx, "request.get", map[string]string{"accesskey": accessKey})
	if err != nil {
		return nil, err
	}

	var result Request
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil, fmt.Errorf("failed to parse request: %w", err)
	}

	return &result, nil
}

func (c *Client) UpdateRequest(ctx context.Context, params map[string]string) (*Request, error) {
	if params["accesskey"] == "" {
		return nil, fmt.Errorf("accesskey is required")
	}
	if params["tNote"] == "" {
		return nil, fmt.Errorf("tNote is required")
	}

	data, err := c.DoRaw(ctx, "request.update", params)
	if err != nil {
		return nil, err
	}

	var result Request
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil, fmt.Errorf("failed to parse request: %w", err)
	}

	return &result, nil
}

func (c *Client) GetCategories(ctx context.Context) ([]Category, error) {
	resp, err := c.Do(ctx, "request.getCategories", nil)
	if err != nil {
		return nil, err
	}
	return resp.Categories, nil
}

func (c *Client) GetCustomFields(ctx context.Context) ([]CustomField, error) {
	resp, err := c.Do(ctx, "request.getCustomFields", nil)
	if err != nil {
		return nil, err
	}
	return resp.CustomFields, nil
}

func (c *Client) GetCustomerRequests(ctx context.Context, email, password string) ([]Request, error) {
	resp, err := c.Do(ctx, "customer.getRequests", map[string]string{
		"sEmail":    email,
		"sPassword": password,
	})
	if err != nil {
		return nil, err
	}
	CalculateRequestAges(resp.Requests)
	return resp.Requests, nil
}
