package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"strings"

	"github.com/helpspot/helpspotgo"
	"github.com/jedib0t/go-pretty/v6/table"
	"github.com/urfave/cli/v2"
)

var (
	version   = "1.0.0"
	baseURL   string
	username  string
	password  string
	apiKey    string
	output    string
	columns   string
	apiOutput string
	debug     bool
	configDir string
)

func main() {
	app := &cli.App{
		Name:     "helpspot",
		Version:  version,
		Usage:    "HelpSpot CLI - Interact with HelpSpot API",
		Before:   loadConfig,
		Flags:    globalFlags(),
		Commands: commands(),
		Action:   runVersion,
	}

	if err := app.Run(os.Args); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func globalFlags() []cli.Flag {
	return []cli.Flag{
		&cli.StringFlag{
			Name:        "base-url",
			Usage:       "HelpSpot base URL",
			EnvVars:     []string{"HELSPOT_BASE_URL"},
			Destination: &baseURL,
		},
		&cli.StringFlag{
			Name:        "username",
			Usage:       "Username for basic auth",
			EnvVars:     []string{"HELSPOT_USERNAME"},
			Destination: &username,
		},
		&cli.StringFlag{
			Name:        "password",
			Usage:       "Password for basic auth",
			EnvVars:     []string{"HELSPOT_PASSWORD"},
			Destination: &password,
		},
		&cli.StringFlag{
			Name:        "api-key",
			Usage:       "API key for Bearer auth",
			EnvVars:     []string{"HELSPOT_API_KEY"},
			Destination: &apiKey,
		},
		&cli.StringFlag{
			Name:        "output",
			Usage:       "Output format: json, table",
			Value:       "json",
			Destination: &output,
		},
		&cli.StringFlag{
			Name:        "columns",
			Usage:       "Columns to display in table output (comma-separated)",
			Destination: &columns,
		},
		&cli.BoolFlag{
			Name:        "debug",
			Usage:       "Enable debug mode",
			Destination: &debug,
		},
		&cli.StringFlag{
			Name:        "config-dir",
			Usage:       "Config directory",
			EnvVars:     []string{"HELSPOT_CONFIG_DIR"},
			Destination: &configDir,
		},
	}
}

func loadConfig(c *cli.Context) error {
	if baseURL == "" {
		cfg, err := helpspotgo.LoadConfigFile()
		if err == nil && cfg != nil {
			if baseURL == "" && cfg.BaseURL != "" {
				baseURL = cfg.BaseURL
			}
			if username == "" && cfg.Username != "" {
				username = cfg.Username
			}
			if password == "" && cfg.Password != "" {
				password = cfg.Password
			}
			if apiKey == "" && cfg.APIKey != "" {
				apiKey = cfg.APIKey
			}
			if output == "" && cfg.Output != "" {
				output = cfg.Output
			}
		}
	}
	return nil
}

func getClient() (*helpspotgo.Client, error) {
	if apiOutput == "" {
		apiOutput = "json"
	}
	opts := []helpspotgo.Option{
		helpspotgo.WithBaseURL(baseURL),
		helpspotgo.WithOutput(apiOutput),
		helpspotgo.WithDebug(debug),
	}

	if apiKey != "" {
		opts = append(opts, helpspotgo.WithAPIKey(apiKey))
	} else if username != "" && password != "" {
		opts = append(opts, helpspotgo.WithBasicAuth(username, password))
	}

	return helpspotgo.NewClient(opts...)
}

func commands() []*cli.Command {
	return []*cli.Command{
		configCommands(),
		requestCommands(),
		categoryCommands(),
		customFieldCommands(),
		kbCommands(),
		forumCommands(),
		{
			Name:   "version",
			Usage:  "Get API version",
			Action: runVersion,
		},
		{
			Name:   "field-labels",
			Usage:  "Get field labels",
			Action: runFieldLabels,
		},
	}
}

func configCommands() *cli.Command {
	return &cli.Command{
		Name:  "config",
		Usage: "Manage configuration",
		Subcommands: []*cli.Command{
			{
				Name:   "init",
				Usage:  "Initialize config file",
				Action: runConfigInit,
			},
			{
				Name:   "show",
				Usage:  "Show current config",
				Action: runConfigShow,
			},
		},
	}
}

func requestCommands() *cli.Command {
	return &cli.Command{
		Name:  "request",
		Usage: "Manage requests",
		Subcommands: []*cli.Command{
			{
				Name:      "create",
				Usage:     "Create a new request",
				ArgsUsage: "[--note NOTE] [--email EMAIL] [--category ID]",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "note", Aliases: []string{"n"}, Usage: "Request note/body", Required: true},
					&cli.StringFlag{Name: "email", Aliases: []string{"e"}, Usage: "Customer email"},
					&cli.StringFlag{Name: "first-name", Usage: "Customer first name"},
					&cli.StringFlag{Name: "last-name", Usage: "Customer last name"},
					&cli.StringFlag{Name: "phone", Usage: "Customer phone"},
					&cli.StringFlag{Name: "user-id", Usage: "Customer user ID"},
					&cli.StringFlag{Name: "category", Aliases: []string{"c"}, Usage: "Category ID"},
					&cli.StringFlag{Name: "title", Aliases: []string{"t"}, Usage: "Request title"},
				},
				Action: runRequestCreate,
			},
			{
				Name:      "get",
				Usage:     "Get request by access key",
				ArgsUsage: "ACCESS_KEY",
				Action:    runRequestGet,
			},
			{
				Name:      "get-id",
				Usage:     "Get request by ID (private)",
				ArgsUsage: "REQUEST_ID",
				Action:    runRequestGetByID,
			},
			{
				Name:  "update",
				Usage: "Update a request",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "access-key", Aliases: []string{"k"}, Usage: "Access key", Required: true},
					&cli.StringFlag{Name: "note", Aliases: []string{"n"}, Usage: "Note to add", Required: true},
				},
				Action: runRequestUpdate,
			},
			{
				Name:  "list",
				Usage: "List requests (filtered)",
				Flags: []cli.Flag{
					&cli.StringFlag{Name: "filter", Aliases: []string{"f"}, Usage: "Filter ID"},
					&cli.StringFlag{Name: "search", Aliases: []string{"s"}, Usage: "Search text"},
					&cli.IntFlag{Name: "limit", Usage: "Limit results"},
				},
				Action: runRequestList,
			},
		},
	}
}

func categoryCommands() *cli.Command {
	return &cli.Command{
		Name:  "category",
		Usage: "Manage categories",
		Subcommands: []*cli.Command{
			{
				Name:   "list",
				Usage:  "List categories",
				Action: runCategoryList,
			},
		},
	}
}

func customFieldCommands() *cli.Command {
	return &cli.Command{
		Name:  "customfield",
		Usage: "Manage custom fields",
		Subcommands: []*cli.Command{
			{
				Name:   "list",
				Usage:  "List custom fields",
				Action: runCustomFieldList,
			},
		},
	}
}

func kbCommands() *cli.Command {
	return &cli.Command{
		Name:  "kb",
		Usage: "Knowledge base",
		Subcommands: []*cli.Command{
			{
				Name:   "list",
				Usage:  "List knowledge books",
				Action: runKBList,
			},
			{
				Name:      "get",
				Usage:     "Get KB book",
				ArgsUsage: "BOOK_ID",
				Action:    runKBGet,
			},
			{
				Name:      "toc",
				Usage:     "Get book table of contents",
				ArgsUsage: "BOOK_ID",
				Action:    runKBTOC,
			},
			{
				Name:      "page",
				Usage:     "Get KB page",
				ArgsUsage: "PAGE_ID",
				Action:    runKBPage,
			},
			{
				Name:      "search",
				Usage:     "Search knowledge base",
				ArgsUsage: "QUERY",
				Action:    runKBSearch,
			},
		},
	}
}

func forumCommands() *cli.Command {
	return &cli.Command{
		Name:  "forum",
		Usage: "Forums",
		Subcommands: []*cli.Command{
			{
				Name:   "list",
				Usage:  "List forums",
				Action: runForumList,
			},
			{
				Name:      "topics",
				Usage:     "List forum topics",
				ArgsUsage: "FORUM_ID",
				Action:    runForumTopics,
			},
			{
				Name:      "posts",
				Usage:     "List topic posts",
				ArgsUsage: "TOPIC_ID",
				Action:    runForumPosts,
			},
		},
	}
}

func runVersion(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	info, err := client.GetVersion(ctx)
	if err != nil {
		return err
	}

	return printOutput(info)
}

func runFieldLabels(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	labels, err := client.GetFieldLabels(ctx)
	if err != nil {
		return err
	}

	return printOutput(labels)
}

func runConfigInit(c *cli.Context) error {
	cfg := &helpspotgo.ConfigFile{
		BaseURL:  baseURL,
		Username: username,
		Password: password,
		APIKey:   apiKey,
		Output:   output,
		Timeout:  30,
	}

	if cfg.BaseURL == "" {
		fmt.Print("Enter HelpSpot base URL: ")
		fmt.Scanln(&cfg.BaseURL)
	}
	if cfg.Username == "" {
		fmt.Print("Enter username: ")
		fmt.Scanln(&cfg.Username)
	}
	if cfg.Password == "" {
		fmt.Print("Enter password: ")
		fmt.Scanln(&cfg.Password)
	}

	if err := helpspotgo.SaveConfigFile(cfg); err != nil {
		return fmt.Errorf("failed to save config: %w", err)
	}

	fmt.Println("Config saved successfully")
	return nil
}

func runConfigShow(c *cli.Context) error {
	cfg, err := helpspotgo.LoadConfigFile()
	if err != nil {
		return err
	}
	if cfg == nil {
		fmt.Println("No config found")
		return nil
	}

	return printOutput(cfg)
}

func runRequestCreate(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	params := map[string]string{
		"tNote": c.String("note"),
	}

	if email := c.String("email"); email != "" {
		params["sEmail"] = email
	}
	if firstName := c.String("first-name"); firstName != "" {
		params["sFirstName"] = firstName
	}
	if lastName := c.String("last-name"); lastName != "" {
		params["sLastName"] = lastName
	}
	if phone := c.String("phone"); phone != "" {
		params["sPhone"] = phone
	}
	if userID := c.String("user-id"); userID != "" {
		params["sUserId"] = userID
	}
	if category := c.String("category"); category != "" {
		params["xCategory"] = category
	}
	if title := c.String("title"); title != "" {
		params["sTitle"] = title
	}

	ctx := context.Background()
	req, err := client.CreateRequest(ctx, params)
	if err != nil {
		return err
	}

	return printOutput(req)
}

func runRequestGet(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("access key required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	req, err := client.GetRequest(ctx, c.Args().First())
	if err != nil {
		return err
	}

	return printOutput(req)
}

func runRequestGetByID(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("request ID required")
	}

	var requestID int
	fmt.Sscanf(c.Args().First(), "%d", &requestID)

	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	req, err := client.GetPrivateRequest(ctx, requestID)
	if err != nil {
		return err
	}

	return printOutput(req)
}

func runRequestUpdate(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	params := map[string]string{
		"accesskey": c.String("access-key"),
		"tNote":     c.String("note"),
	}

	ctx := context.Background()
	req, err := client.UpdateRequest(ctx, params)
	if err != nil {
		return err
	}

	return printOutput(req)
}

func runRequestList(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	params := make(map[string]string)
	if filter := c.String("filter"); filter != "" {
		params["xFilter"] = filter
	}
	if search := c.String("search"); search != "" {
		params["sSearch"] = search
	}
	if limit := c.Int("limit"); limit > 0 {
		params["limit"] = fmt.Sprint(limit)
	}

	ctx := context.Background()
	requests, err := client.SearchPrivateRequests(ctx, params)
	if err != nil {
		return err
	}

	return printOutput(requests)
}

func runCategoryList(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	categories, err := client.GetCategories(ctx)
	if err != nil {
		return err
	}

	return printOutput(categories)
}

func runCustomFieldList(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	fields, err := client.GetCustomFields(ctx)
	if err != nil {
		return err
	}

	return printOutput(fields)
}

func runKBList(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	books, err := client.ListKBBooks(ctx)
	if err != nil {
		return err
	}

	return printOutput(books)
}

func runKBGet(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("book ID required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	var bookID int
	fmt.Sscanf(c.Args().First(), "%d", &bookID)

	ctx := context.Background()
	book, err := client.GetKBBook(ctx, bookID)
	if err != nil {
		return err
	}

	return printOutput(book)
}

func runKBTOC(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("book ID required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	var bookID int
	fmt.Sscanf(c.Args().First(), "%d", &bookID)

	ctx := context.Background()
	book, err := client.GetKBBookTOC(ctx, bookID)
	if err != nil {
		return err
	}

	return printOutput(book)
}

func runKBPage(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("page ID required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	var pageID int
	fmt.Sscanf(c.Args().First(), "%d", &pageID)

	ctx := context.Background()
	page, err := client.GetKBPage(ctx, pageID)
	if err != nil {
		return err
	}

	return printOutput(page)
}

func runKBSearch(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("search query required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	results, err := client.SearchKB(ctx, c.Args().First())
	if err != nil {
		return err
	}

	return printOutput(results)
}

func runForumList(c *cli.Context) error {
	client, err := getClient()
	if err != nil {
		return err
	}

	ctx := context.Background()
	forums, err := client.ListForums(ctx)
	if err != nil {
		return err
	}

	return printOutput(forums)
}

func runForumTopics(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("forum ID required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	var forumID int
	fmt.Sscanf(c.Args().First(), "%d", &forumID)

	ctx := context.Background()
	topics, err := client.GetForumTopics(ctx, forumID)
	if err != nil {
		return err
	}

	return printOutput(topics)
}

func runForumPosts(c *cli.Context) error {
	if c.Args().Len() == 0 {
		return fmt.Errorf("topic ID required")
	}

	client, err := getClient()
	if err != nil {
		return err
	}

	var topicID int
	fmt.Sscanf(c.Args().First(), "%d", &topicID)

	ctx := context.Background()
	posts, err := client.GetTopicPosts(ctx, topicID)
	if err != nil {
		return err
	}

	return printOutput(posts)
}

func printOutput(v any) error {
	if output == "json" {
		data, err := json.MarshalIndent(v, "", "  ")
		if err != nil {
			return err
		}
		fmt.Println(string(data))
		return nil
	}

	if output == "table" {
		return printTable(v)
	}

	data, err := json.Marshal(v)
	if err != nil {
		return err
	}
	fmt.Println(string(data))
	return nil
}

func printTable(v any) error {
	rv := reflect.ValueOf(v)

	if rv.Kind() == reflect.Ptr {
		rv = rv.Elem()
	}

	if rv.Kind() == reflect.Slice && rv.Len() > 0 {
		firstElem := rv.Index(0)
		if firstElem.Kind() == reflect.Ptr {
			firstElem = firstElem.Elem()
		}
		if firstElem.Type().Name() == "Request" && columns == "" {
			columns = "XRequest,Title,Status,Created"
		}
	}

	switch rv.Kind() {
	case reflect.Slice:
		return printTableSlice(rv)
	case reflect.Map:
		return printTableMap(rv)
	default:
		return printTableSingle(v)
	}
}

func printTableSlice(rv reflect.Value) error {
	if rv.Len() == 0 {
		fmt.Println("No data")
		return nil
	}

	firstElem := rv.Index(0)
	if firstElem.Kind() == reflect.Ptr {
		firstElem = firstElem.Elem()
	}

	headers, rows := extractHeadersAndRows(rv, firstElem)

	t := table.NewWriter()
	t.SetOutputMirror(os.Stdout)
	t.SetStyle(table.StyleRounded)

	headerRow := table.Row{}
	for _, h := range headers {
		headerRow = append(headerRow, h)
	}
	t.AppendHeader(headerRow)

	for _, row := range rows {
		tRow := table.Row{}
		for _, cell := range row {
			tRow = append(tRow, cell)
		}
		t.AppendRow(tRow)
	}

	t.Render()
	return nil
}

func extractHeadersAndRows(rv reflect.Value, firstElem reflect.Value) ([]string, [][]string) {
	var headers []string
	var rows [][]string

	var columnFilter map[string]bool
	if columns != "" {
		columnFilter = make(map[string]bool)
		for _, col := range strings.Split(columns, ",") {
			columnFilter[strings.TrimSpace(col)] = true
		}
	}

	if firstElem.Kind() == reflect.Struct {
		t := firstElem.Type()
		var fieldIndices []int
		for i := 0; i < t.NumField(); i++ {
			field := t.Field(i)
			if columnFilter == nil || columnFilter[field.Name] {
				headers = append(headers, field.Name)
				fieldIndices = append(fieldIndices, i)
			}
		}

		for i := 0; i < rv.Len(); i++ {
			elem := rv.Index(i)
			if elem.Kind() == reflect.Ptr {
				elem = elem.Elem()
			}
			var row []string
			for _, idx := range fieldIndices {
				val := elem.Field(idx).String()
				row = append(row, val)
			}
			rows = append(rows, row)
		}
	} else if firstElem.Kind() == reflect.Map {
		for i := 0; i < rv.Len(); i++ {
			elem := rv.Index(i)
			if elem.Kind() == reflect.Ptr {
				elem = elem.Elem()
			}
			if elem.Kind() == reflect.Map {
				keys := elem.MapKeys()
				if len(headers) == 0 {
					for _, k := range keys {
						key := fmt.Sprintf("%v", k.Interface())
						if columnFilter == nil || columnFilter[key] {
							headers = append(headers, key)
						}
					}
				}
				var row []string
				for _, h := range headers {
					for _, k := range keys {
						if fmt.Sprintf("%v", k.Interface()) == h {
							val := elem.MapIndex(k)
							row = append(row, fmt.Sprintf("%v", val.Interface()))
							break
						}
					}
				}
				rows = append(rows, row)
			}
		}
	}

	return headers, rows
}

func printTableMap(rv reflect.Value) error {
	keys := rv.MapKeys()
	if len(keys) == 0 {
		fmt.Println("No data")
		return nil
	}

	t := table.NewWriter()
	t.SetOutputMirror(os.Stdout)
	t.SetStyle(table.StyleRounded)
	t.AppendHeader(table.Row{"Key", "Value"})

	for _, k := range keys {
		key := fmt.Sprintf("%v", k.Interface())
		val := fmt.Sprintf("%v", rv.MapIndex(k).Interface())
		t.AppendRow(table.Row{key, val})
	}

	t.Render()
	return nil
}

func printTableSingle(v any) error {
	rv := reflect.ValueOf(v)
	if rv.Kind() == reflect.Ptr {
		rv = rv.Elem()
	}

	t := table.NewWriter()
	t.SetOutputMirror(os.Stdout)
	t.SetStyle(table.StyleRounded)

	if rv.Kind() == reflect.Struct {
		t.AppendHeader(table.Row{"Field", "Value"})
		tv := rv.Type()
		for i := 0; i < tv.NumField(); i++ {
			field := tv.Field(i)
			val := rv.Field(i).String()
			t.AppendRow(table.Row{field.Name, val})
		}
	} else if rv.Kind() == reflect.Map {
		t.AppendHeader(table.Row{"Key", "Value"})
		keys := rv.MapKeys()
		for _, k := range keys {
			key := fmt.Sprintf("%v", k.Interface())
			val := fmt.Sprintf("%v", rv.MapIndex(k).Interface())
			t.AppendRow(table.Row{key, val})
		}
	} else {
		t.AppendHeader(table.Row{"Value"})
		t.AppendRow(table.Row{fmt.Sprintf("%v", v)})
	}

	t.Render()
	return nil
}
