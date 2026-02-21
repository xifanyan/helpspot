package helpspotgo

import (
	"context"
	"fmt"
)

type FilterResult struct {
	XFilter  int       `json:"xFilter"`
	Name     string    `json:"sName"`
	Requests []Request `json:"requests,omitempty"`
}

func (c *Client) GetFilters(ctx context.Context) ([]Filter, error) {
	resp, err := c.Do(ctx, "private.filter.get", nil)
	if err != nil {
		return nil, err
	}
	return resp.Filters, nil
}

func (c *Client) GetFilterColumnNames(ctx context.Context, filterID int) ([]string, error) {
	params := map[string]string{"xFilter": fmt.Sprint(filterID)}
	resp, err := c.Do(ctx, "private.filter.getColumnNames", params)
	if err != nil {
		return nil, err
	}
	return resp.FilterColumns, nil
}

func (c *Client) GetFilterStream(ctx context.Context, filterID int, params map[string]string) ([]Request, error) {
	if params == nil {
		params = make(map[string]string)
	}
	params["xFilter"] = fmt.Sprint(filterID)
	resp, err := c.Do(ctx, "private.filter.getStream", params)
	if err != nil {
		return nil, err
	}
	return resp.Requests, nil
}

func (c *Client) GetUserFilters(ctx context.Context) ([]Filter, error) {
	resp, err := c.Do(ctx, "private.user.getFilters", nil)
	if err != nil {
		return nil, err
	}
	return resp.Filters, nil
}

func (c *Client) GetUserPreferences(ctx context.Context) (map[string]any, error) {
	resp, err := c.Do(ctx, "private.user.preferences", nil)
	if err != nil {
		return nil, err
	}
	return resp.Preferences, nil
}

func (c *Client) GetActiveStaff(ctx context.Context) ([]Staff, error) {
	resp, err := c.Do(ctx, "private.util.getActiveStaff", nil)
	if err != nil {
		return nil, err
	}
	return resp.Staff, nil
}
