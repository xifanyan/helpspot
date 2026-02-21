package helpspotgo

import (
	"context"
	"fmt"
)

func (c *Client) ListForums(ctx context.Context) ([]Forum, error) {
	resp, err := c.Do(ctx, "forums.list", nil)
	if err != nil {
		return nil, err
	}
	return resp.Forums, nil
}

func (c *Client) GetForum(ctx context.Context, forumID int) (*Forum, error) {
	resp, err := c.Do(ctx, "forums.get", map[string]string{"xForum": fmt.Sprint(forumID)})
	if err != nil {
		return nil, err
	}
	return &resp.Forum, nil
}

func (c *Client) GetForumTopics(ctx context.Context, forumID int) ([]Topic, error) {
	resp, err := c.Do(ctx, "forums.getTopics", map[string]string{"xForum": fmt.Sprint(forumID)})
	if err != nil {
		return nil, err
	}
	return resp.Topics, nil
}

func (c *Client) GetTopicPosts(ctx context.Context, topicID int) ([]Post, error) {
	resp, err := c.Do(ctx, "forums.getPosts", map[string]string{"xTopic": fmt.Sprint(topicID)})
	if err != nil {
		return nil, err
	}
	return resp.Posts, nil
}

func (c *Client) CreateForumTopic(ctx context.Context, params map[string]string) (*Topic, error) {
	if params["sTitle"] == "" {
		return nil, fmt.Errorf("sTitle is required")
	}
	if params["tPost"] == "" {
		return nil, fmt.Errorf("tPost is required")
	}

	resp, err := c.Do(ctx, "forums.createTopic", params)
	if err != nil {
		return nil, err
	}
	return &resp.Topic, nil
}

func (c *Client) CreateForumPost(ctx context.Context, params map[string]string) error {
	if params["xTopic"] == "" {
		return fmt.Errorf("xTopic is required")
	}
	if params["tPost"] == "" {
		return fmt.Errorf("tPost is required")
	}

	_, err := c.Do(ctx, "forums.createPost", params)
	return err
}

func (c *Client) SearchForums(ctx context.Context, query string) ([]Forum, error) {
	resp, err := c.Do(ctx, "forums.search", map[string]string{"sSearch": query})
	if err != nil {
		return nil, err
	}
	return resp.Forums, nil
}
