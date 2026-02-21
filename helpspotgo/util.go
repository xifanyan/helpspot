package helpspotgo

import (
	"context"
)

func (c *Client) GetFieldLabels(ctx context.Context) (map[string]any, error) {
	resp, err := c.Do(ctx, "util.getFieldLabels", nil)
	if err != nil {
		return nil, err
	}
	return resp.FieldLabels, nil
}
