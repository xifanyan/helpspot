# Go Implementation Details

**Status:** Complete

| HTTP Client | CLI Framework | Config Location |
|-------------|---------------|-----------------|
| resty | urfave/cli | ~/.config/helpspot/config.json |

## Dependencies
- `github.com/resty/resty/v2` - HTTP client
- `github.com/urfave/cli/v2` - CLI framework

## Project Structure
```
helpspotgo/
├── client.go               # HTTP client (resty)
├── config.go               # Config file handling
├── errors.go               # Error types
├── types.go                # Data models
├── request.go              # Public request methods
├── private_request.go      # Private request methods
├── kb.go                   # Knowledge base methods
├── forum.go                # Forum methods
├── private_filter.go       # Filter/user methods
├── util.go                 # Utility methods
├── logger.go               # Logging utilities
├── cmd/
│   └── main.go            # CLI application
├── helpspot.exe            # CLI binary
├── go.mod
└── go.sum
```

## Build Rules

- Always use `-ldflags="-s -w"` to optimize the binary (strip symbols and debugging info)
