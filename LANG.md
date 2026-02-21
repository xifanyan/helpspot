# Language-Specific Implementation Details

This file documents the implementation choices for each language in the helpspot client library ecosystem.

## Package Choices by Language

| Language | HTTP Client | CLI Framework | Config Location |
|----------|-------------|---------------|-----------------|
| Go | resty | urfave/cli | ~/.config/helpspot/config.json |
| Python | httpx | click | ~/.config/helpspot/config.json |
| Rust | reqwest | clap | ~/.config/helpspot/config.json |

## Go Implementation

**Status:** Complete

### Dependencies
- `github.com/resty/resty/v2` - HTTP client
- `github.com/urfave/cli/v2` - CLI framework

### Project Structure
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
├── cmd/
│   └── main.go            # CLI application
├── helpspot.exe            # CLI binary
├── go.mod
└── go.sum
```

## Python Implementation

**Status:** Planned

### Dependencies
- `httpx` - HTTP client
- `click` - CLI framework

### Project Structure
```
helpspotpy/
├── client.py
├── config.py
├── models.py
├── api/
├── cli/
└── pyproject.toml
```

## Rust Implementation

**Status:** Planned

### Dependencies
- `reqwest` - HTTP client
- `clap` - CLI framework

### Project Structure
```
helpspotrs/
├── src/
│   ├── client.rs
│   ├── config.rs
│   ├── types.rs
│   └── cli/
└── Cargo.toml
```
