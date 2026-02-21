package helpspotgo

import (
	"context"
	"encoding/json"
	"fmt"
)

func (c *Client) ListKBBooks(ctx context.Context) ([]KBBook, error) {
	data, err := c.DoRaw(ctx, "kb.list", nil)
	if err != nil {
		return nil, err
	}

	var result KBBooksResponse
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil, fmt.Errorf("failed to parse KB books: %w", err)
	}

	return result.Books, nil
}

func (c *Client) GetKBBook(ctx context.Context, bookID int) (*KBBook, error) {
	resp, err := c.Do(ctx, "kb.get", map[string]string{"xKBBook": fmt.Sprint(bookID)})
	if err != nil {
		return nil, err
	}
	return &resp.KBBook, nil
}

func (c *Client) GetKBBookTOC(ctx context.Context, bookID int) (*KBBook, error) {
	resp, err := c.Do(ctx, "kb.getBookTOC", map[string]string{"xKBBook": fmt.Sprint(bookID)})
	if err != nil {
		return nil, err
	}
	return &resp.KBBook, nil
}

func (c *Client) GetKBPage(ctx context.Context, pageID int) (*KBPage, error) {
	resp, err := c.Do(ctx, "kb.getPage", map[string]string{"xKBPage": fmt.Sprint(pageID)})
	if err != nil {
		return nil, err
	}
	return &resp.KBPage, nil
}

func (c *Client) SearchKB(ctx context.Context, query string) ([]KBPage, error) {
	resp, err := c.Do(ctx, "kb.search", map[string]string{"sSearch": query})
	if err != nil {
		return nil, err
	}
	return resp.KBSearch, nil
}

func (c *Client) VoteKBPageHelpful(ctx context.Context, pageID int) error {
	_, err := c.Do(ctx, "kb.voteHelpful", map[string]string{"xKBPage": fmt.Sprint(pageID)})
	return err
}

func (c *Client) VoteKBPageNotHelpful(ctx context.Context, pageID int) error {
	_, err := c.Do(ctx, "kb.voteNotHelpful", map[string]string{"xKBPage": fmt.Sprint(pageID)})
	return err
}
