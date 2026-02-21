package helpspotgo

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/go-resty/resty/v2"
)

const (
	APIVersion = "1.0.0"
	basePath   = "/api/index.php"
)

type Client struct {
	client *resty.Client
	config *Config
}

type Config struct {
	BaseURL  string
	APIKey   string
	Username string
	Password string
	Output   string
	Timeout  time.Duration
	Debug    bool
}

type Option func(*Config)

func WithBaseURL(baseURL string) Option {
	return func(c *Config) {
		c.BaseURL = baseURL
	}
}

func WithAPIKey(apiKey string) Option {
	return func(c *Config) {
		c.APIKey = apiKey
	}
}

func WithBasicAuth(username, password string) Option {
	return func(c *Config) {
		c.Username = username
		c.Password = password
	}
}

func WithOutput(output string) Option {
	return func(c *Config) {
		c.Output = output
	}
}

func WithTimeout(timeout time.Duration) Option {
	return func(c *Config) {
		c.Timeout = timeout
	}
}

func WithDebug(debug bool) Option {
	return func(c *Config) {
		c.Debug = debug
	}
}

func NewClient(opts ...Option) (*Client, error) {
	cfg := &Config{
		BaseURL: "http://localhost",
		Output:  "json",
		Timeout: 30 * time.Second,
		Debug:   false,
	}

	for _, opt := range opts {
		opt(cfg)
	}

	if cfg.BaseURL == "" {
		return nil, ErrMissingBaseURL
	}

	client := resty.New()
	client.SetBaseURL(cfg.BaseURL)
	client.SetTimeout(cfg.Timeout)
	client.SetDebug(cfg.Debug)
	client.SetHeader("Content-Type", "application/x-www-form-urlencoded")

	if cfg.APIKey != "" {
		client.SetHeader("Authorization", "Bearer "+cfg.APIKey)
	} else if cfg.Username != "" && cfg.Password != "" {
		client.SetBasicAuth(cfg.Username, cfg.Password)
	}

	return &Client{
		client: client,
		config: cfg,
	}, nil
}

func NewClientFromConfig(config *ConfigFile, opts ...Option) (*Client, error) {
	cfg := &Config{
		BaseURL:  config.BaseURL,
		Username: config.Username,
		Password: config.Password,
		APIKey:   config.APIKey,
		Output:   config.Output,
		Timeout:  time.Duration(config.Timeout) * time.Second,
		Debug:    false,
	}

	if cfg.Output == "" {
		cfg.Output = "json"
	}
	if cfg.Timeout == 0 {
		cfg.Timeout = 30 * time.Second
	}

	for _, opt := range opts {
		opt(cfg)
	}

	return NewClient(
		WithBaseURL(cfg.BaseURL),
		WithBasicAuth(cfg.Username, cfg.Password),
		WithAPIKey(cfg.APIKey),
		WithOutput(cfg.Output),
		WithTimeout(cfg.Timeout),
		WithDebug(cfg.Debug),
	)
}

func (c *Client) buildURL(method string) string {
	return c.client.BaseURL + basePath + "?method=" + method + "&output=" + c.config.Output
}

func (c *Client) isPostMethod(method string) bool {
	publicPostMethods := map[string]bool{
		"request.create":     true,
		"request.update":     true,
		"forums.createTopic": true,
		"forums.createPost":  true,
	}
	privatePostMethods := map[string]bool{
		"private.request.get":    false,
		"private.request.search": false,
	}
	if !privatePostMethods[method] && strings.HasPrefix(method, "private.") {
		return true
	}
	return publicPostMethods[method]
}

func (c *Client) Do(ctx context.Context, method string, params map[string]string) (*Response, error) {
	url := c.buildURL(method)

	var resp *resty.Response
	var err error

	if c.isPostMethod(method) {
		allParams := make(map[string]string)
		allParams["method"] = method
		for k, v := range params {
			allParams[k] = v
		}
		resp, err = c.client.R().
			SetContext(ctx).
			SetFormData(allParams).
			Post(url)
	} else if len(params) > 0 {
		resp, err = c.client.R().
			SetContext(ctx).
			SetQueryParams(params).
			Get(url)
	} else {
		resp, err = c.client.R().
			Get(url)
	}

	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}

	if resp.StatusCode() >= 400 {
		return nil, c.parseError(resp.Body(), resp.StatusCode())
	}

	var response Response
	if err := c.client.JSONUnmarshal(resp.Body(), &response); err != nil {
		if c.config.Output == "xml" {
			return &Response{Raw: string(resp.Body())}, nil
		}
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return &response, nil
}

func (c *Client) DoRaw(ctx context.Context, method string, params map[string]string) (string, error) {
	url := c.buildURL(method)

	var resp *resty.Response
	var err error

	// Use GET for private request get and search, POST for other private methods
	if method == "private.request.get" || method == "private.request.search" {
		resp, err = c.client.R().
			SetContext(ctx).
			SetQueryParams(params).
			Get(url)
	} else if c.isPostMethod(method) {
		resp, err = c.client.R().
			SetContext(ctx).
			SetFormData(params).
			Post(url)
	} else {
		resp, err = c.client.R().
			SetContext(ctx).
			SetQueryParams(params).
			Get(url)
	}

	if err != nil {
		return "", fmt.Errorf("request failed: %w", err)
	}

	if resp.StatusCode() >= 400 {
		return "", c.parseError(resp.Body(), resp.StatusCode())
	}

	return string(resp.Body()), nil
}

func (c *Client) GetVersion(ctx context.Context) (*VersionResponse, error) {
	data, err := c.DoRaw(ctx, "version", nil)
	if err != nil {
		return nil, err
	}

	var version VersionResponse
	if err := json.Unmarshal([]byte(data), &version); err != nil {
		return nil, fmt.Errorf("failed to parse version: %w", err)
	}
	return &version, nil
}

func (c *Client) GetPrivateVersion(ctx context.Context) (*VersionResponse, error) {
	data, err := c.DoRaw(ctx, "private.version", nil)
	if err != nil {
		return nil, err
	}

	var version VersionResponse
	if err := json.Unmarshal([]byte(data), &version); err != nil {
		return nil, fmt.Errorf("failed to parse version: %w", err)
	}
	return &version, nil
}
