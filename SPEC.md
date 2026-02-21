# HelpSpot Client Library - Project Specification

## HelpSpot Service Summary

**HelpSpot** is a help desk/customer service software by UserScape, Inc. (est. 2004). It provides email-based customer support with a unified inbox, knowledge base, self-service portal, and reporting.

### Core Features
- **Shared Inbox** - Team collaboration with unified view of all support communications
- **Ticket Management** - Create, update, track, merge, and assign support requests
- **Knowledge Base** - Self-service documentation/articles (KB Books/Pages)
- **Customer Portal** - End-users submit/track requests, search knowledge base
- **Forums** - Community discussion boards
- **Reporting** - Real-time analytics on ticket volume, response times, agent performance
- **Custom Fields** - Flexible data capture for tickets
- **Filters** - Saved search queries for organizing requests

### API Access
- **Public API** - No authentication required (like the customer portal)
- **Private API** - Staff authentication required (full system access)
- **Return Formats** - XML (default), JSON, Serialized PHP
- **Authentication** - Basic Auth or API Key (Bearer token)

---

## Overview

**Project Name:** helpspot - HelpSpot REST API Client Library

**Goal:** A multi-language client library ecosystem for the HelpSpot help desk REST API, with CLI tools for common operations.

**Target Users:** Developers integrating HelpSpot, Support teams using CLI

---

## Package Choices by Language

| Language | HTTP Client | CLI Framework | Config Location |
|----------|-------------|---------------|-----------------|
| Go | resty | urfave/cli | ~/.config/helpspot/config.json |
| Python | httpx | click | ~/.config/helpspot/config.json |
| Rust | reqwest | clap | ~/.config/helpspot/config.json |

---

## CLI Command Structure

### Global Options
```
--config PATH    Config file path (default: ~/.config/helpspot/config.json)
--output FORMAT  Output format: json, xml, table (default: json)
--verbose        Enable verbose logging
--help           Show help
```

### Command Hierarchy

```
helpspot
├── config
│   ├── init          # Initialize config file
│   ├── show          # Show current config
│   └── edit          # Edit config file
├── version           # Get API version
├── request
│   ├── create       # Create new request
│   ├── get           # Get request by access key
│   ├── update        # Update existing request
│   ├── search        # Search requests
│   └── list          # List requests (filtered)
├── customer
│   └── requests      # Get customer's requests
├── category
│   └── list          # List categories
├── customfield
│   └── list          # List custom fields
├── kb
│   ├── list          # List knowledge books
│   ├── get           # Get KB article
│   ├── toc           # Get book table of contents
│   └── search        # Search knowledge base
├── forum
│   ├── list          # List forums
│   ├── topics        # List forum topics
│   └── posts         # List topic posts
└── field-labels      # Get field labels
```

### CLI Command Usage Examples

```bash
# ============================================
# CONFIGURATION
# ============================================

# Initialize config interactively
helpspot config init

# Show current config
helpspot config show

# ============================================
# VERSION & INFO
# ============================================

# Get API version
helpspot version

# Get field labels
helpspot field-labels

# ============================================
# REQUEST OPERATIONS
# ============================================

# Create a new request (public API)
helpspot request create --note "Need help with password reset" --email "customer@example.com" --category 1

# Create a new request with more fields
helpspot request create \
  --note "Issue description" \
  --email "customer@example.com" \
  --first-name "John" \
  --last-name "Doe" \
  --category 1

# Get request by access key (public API)
# The access key is a unique identifier sent to the customer
helpspot request get 12345ABCDE

# Get request by internal ID (private API - requires auth)
helpspot request get-id 2166118

# Update a request (add note)
helpspot request update --id 2166118 --note "Additional information..."

# List/search requests (private API - requires auth)
helpspot request list
helpspot request list --search "LTCSD"
helpspot request list --search "LTCSD" --limit 10
helpspot request list --filter 5              # By filter ID
helpspot request list --limit 25               # Limit results

# ============================================
# CATEGORIES & FIELDS
# ============================================

# List all categories
helpspot category list

# List all custom fields
helpspot customfield list

# ============================================
# KNOWLEDGE BASE
# ============================================

# Search knowledge base
helpspot kb search "password reset"

# List knowledge books
helpspot kb list

# Get KB book details
helpspot kb get 1

# Get book table of contents
helpspot kb toc 1

# Get KB article/page
helpspot kb page 1

# ============================================
# FORUMS
# ============================================

# List forums
helpspot forum list

# List topics in a forum
helpspot forum topics 1

# List posts in a topic
helpspot forum posts 1

# Search forums
helpspot forum search "installation"

# ============================================
# AUTHENTICATION
# ============================================

# Using command line flags
helpspot --base-url "https://your-helpspot.com" \
         --username "admin@example.com" \
         --password "your-password" \
         request list --search "LTCSD"

# Using environment variables
export HELSPOT_BASE_URL="https://your-helpspot.com"
export HELSPOT_USERNAME="admin@example.com"
export HELSPOT_PASSWORD="your-password"
helpspot request list --search "LTCSD"

# Using API key instead of username/password
export HELSPOT_BASE_URL="https://your-helpspot.com"
export HELSPOT_API_KEY="your-api-key"
helpspot request list --search "LTCSD"

# Using config file (default: ~/.config/helpspot/config.json)
# See Configuration section above

# ============================================
# OUTPUT FORMATS
# ============================================

# JSON output (default)
helpspot --output json request get-id 2166118

# Table output (if supported)
helpspot --output table request list --limit 5

# Debug mode (shows HTTP requests/responses)
helpspot --debug request get-id 2166118
```

---

## Command Reference

### Global Options

| Option | Env Variable | Description |
|--------|--------------|-------------|
| `--base-url` | `HELSPOT_BASE_URL` | HelpSpot base URL |
| `--username` | `HELSPOT_USERNAME` | Username for basic auth |
| `--password` | `HELSPOT_PASSWORD` | Password for basic auth |
| `--api-key` | `HELSPOT_API_KEY` | API key for Bearer auth |
| `--output` | - | Output format: json, table (default: json) |
| `--debug` | - | Enable debug mode |
| `--config-dir` | `HELSPOT_CONFIG_DIR` | Config directory (default: ~/.config/helpspot) |

---

## API Methods (Business Requirements)

### Public Methods (No Auth Required)

| Method | Category | Description |
|--------|----------|-------------|
| `version` | System | Get API version |
| `request.create` | Request | Create new request |
| `request.update` | Request | Update request (add note) |
| `request.get` | Request | Get request by access key |
| `request.getCategories` | Category | List public categories |
| `request.getCustomFields` | CustomField | List public custom fields |
| `customer.getRequests` | Customer | Get customer's requests |
| `kb.list` | KB | List knowledge books |
| `kb.get` | KB | Get KB book |
| `kb.getBookTOC` | KB | Get book table of contents |
| `kb.getPage` | KB | Get KB page/article |
| `kb.search` | KB | Search knowledge base |
| `kb.voteHelpful` | KB | Vote article helpful |
| `kb.voteNotHelpful` | KB | Vote article not helpful |
| `forums.list` | Forum | List forums |
| `forums.get` | Forum | Get forum details |
| `forums.getTopics` | Forum | List forum topics |
| `forums.getPosts` | Forum | List topic posts |
| `forums.createTopic` | Forum | Create new topic |
| `forums.createPost` | Forum | Create new post |
| `forums.search` | Forum | Search forums |
| `util.getFieldLabels` | System | Get field labels |

### Private Methods (Auth Required)

| Method | Category | Description |
|--------|----------|-------------|
| `private.version` | System | Get API version (auth) |
| `private.request.create` | Request | Create request (staff) |
| `private.request.update` | Request | Update request (staff) |
| `private.request.get` | Request | Get request by ID |
| `private.request.multiGet` | Request | Get multiple requests |
| `private.request.search` | Request | Search requests |
| `private.request.getCategories` | Category | List all categories |
| `private.request.getCustomFields` | CustomField | List all custom fields |
| `private.request.getMailboxes` | Request | List mailboxes |
| `private.request.getStatusTypes` | Request | List status types |
| `private.request.getTimeEvents` | Request | Get time events |
| `private.request.addTimeEvent` | Request | Add time event |
| `private.request.subscriptions` | Request | Get subscriptions |
| `private.filter.get` | Filter | Get filters |
| `private.filter.getStream` | Filter | Get filter results |
| `private.user.preferences` | User | Get user preferences |
| `private.util.getActiveStaff` | System | List active staff |
| `private.addressbook.getContacts` | AddressBook | Get contacts |
| `private.addressbook.createContact` | AddressBook | Create contact |

---

## Configuration Specification

### Config File Format
```json
{
  "base_url": "https://your-helpspot.com",
  "username": "admin@example.com",
  "password": "your-password",
  "api_key": "optional-api-key",
  "timeout": 30,
  "output": "json"
}
```

### Config Priority (highest to lowest)
1. Command line flags
2. Environment variables (`HELSPOT_BASE_URL`, `HELSPOT_USERNAME`, `HELSPOT_PASSWORD`, `HELSPOT_API_KEY`)
3. Config file
4. Default values

### Environment Variables
| Variable | Description |
|----------|-------------|
| `HELSPOT_BASE_URL` | HelpSpot API base URL |
| `HELSPOT_USERNAME` | Username for basic auth |
| `HELSPOT_PASSWORD` | Password for basic auth |
| `HELSPOT_API_KEY` | API key for Bearer auth |
| `HELSPOT_CONFIG_DIR` | Custom config directory |

---

## Data Types

### Request
```
- xRequest: int
- accessKey: string
- title: string
- note: string
- firstName: string
- lastName: string
- email: string
- phone: string
- userId: string
- category: string
- xCategory: int
- status: string
- xStatus: int
- urgent: bool
- open: bool
- personAssignedTo: int
- personOpenedBy: int
- fullName: string
- created: timestamp
- updated: timestamp
```

### Category
```
- xCategory: int
- category: string
- customFieldList: []int
```

### CustomField
```
- xCustomField: int
- fieldName: string
- fieldType: string
- isRequired: bool
- textSize: string
- listItems: []string
```

### KBBook
```
- xKBBook: int
- title: string
- pages: []KBPage
```

### KBPage
```
- xKBPage: int
- xKBBook: int
- title: string
- content: string
- pageOrder: int
```

---

## Error Handling

### Error Response Format
```json
{
  "errors": [
    {
      "id": 2,
      "description": "User authentication failed"
    }
  ]
}
```

### Common Error Codes
| Code | Description |
|------|-------------|
| 1 | Unknown error |
| 2 | Authentication failed |
| 3 | Insufficient permissions |
| 4 | Not found |
| 5 | Invalid input |
| 6 | API version mismatch |

---

## Implementation Status

### Phase 1: Foundation (Go: Complete)
- [x] Config file handling (load/save)
- [x] HTTP client with resty (basic, API key auth)
- [x] Error handling (APIError, parseError)
- [x] Data types (Request, Category, CustomField, KB, Forum)
- [x] Go project structure setup

### Phase 2: Public API (Go: Complete)
- [x] version method
- [x] request.create
- [x] request.get
- [x] request.update
- [x] request.getCategories
- [x] request.getCustomFields
- [x] customer.getRequests
- [x] kb.list, kb.get, kb.getBookTOC, kb.getPage
- [x] kb.search
- [x] kb.voteHelpful, kb.voteNotHelpful
- [x] forums.list, forums.get, forums.getTopics, forums.getPosts
- [x] forums.createTopic, forums.createPost, forums.search
- [x] util.getFieldLabels

### Phase 3: Private API (Go: Partial)
- [x] private.request.create, private.request.get, private.request.update
- [x] private.request.multiGet, private.request.search
- [x] private.request.getCategories, private.request.getCustomFields
- [x] private.request.getMailboxes, private.request.getStatusTypes
- [x] private.request.markTrash, private.request.markSpam, private.request.merge
- [x] private.filter.get, private.filter.getColumnNames, private.filter.getStream
- [x] private.user.getFilters, private.user.preferences
- [x] private.util.getActiveStaff
- [ ] private.request.getTimeEvents, private.request.addTimeEvent
- [ ] private.request.subscriptions, private.request.subscribe, private.request.unsubscribe
- [ ] private.addressbook.* methods
- [ ] private.report.* methods

### Phase 4: CLI (Go: Complete)
- [x] config init/show commands
- [x] request create/get/update/list commands
- [x] kb list/get/toc/page/search commands
- [x] category list, customfield list commands
- [x] forum list/topics/posts commands
- [x] field-labels command
- [x] version command
- [x] Output formatting (json)

---

## Project Structure

```
helpspot/
├── SPEC.md                      # This file
├── helpspotgo/                  # Go implementation (complete)
│   ├── client.go               # HTTP client (resty)
│   ├── config.go               # Config file handling
│   ├── errors.go               # Error types
│   ├── types.go                # Data models
│   ├── request.go              # Public request methods
│   ├── private_request.go      # Private request methods
│   ├── kb.go                   # Knowledge base methods
│   ├── forum.go                # Forum methods
│   ├── private_filter.go       # Filter/user methods
│   ├── util.go                 # Utility methods
│   ├── cmd/
│   │   └── main.go             # CLI application
│   ├── helpspot.exe            # CLI binary
│   ├── go.mod
│   └── go.sum
├── helpspotpy/                  # Python implementation (planned)
│   ├── client.py
│   ├── config.py
│   ├── models.py
│   ├── api/
│   ├── cli/
│   └── pyproject.toml
├── helpspotrs/                # Rust implementation (planned)
│   ├── src/
│   │   ├── client.rs
│   │   ├── config.rs
│   │   ├── types.rs
│   │   └── cli/
│   └── Cargo.toml
└── spec/                     # Shared specification (future)
    ├── api.yaml              # OpenAPI-like spec
    └── types.json            # Shared type definitions
```
