# HelpSpot Python Client

A modern Python client library for the [HelpSpot](https://www.helpspot.com/) API, featuring both a Python SDK and a command-line interface (CLI).

## Features

- **Full API Coverage**: Core methods for requests, customers, categories, filters, and more
- **Command-Line Interface**: Manage tickets and resources from your terminal
- **Type Safety**: Built with Pydantic models for robust data validation
- **Modern Python**: Supports Python 3.12+ with type hints
- **Authentication**: Supports both API tokens (recommended) and Basic auth
- **Easy to Use**: Intuitive, Pythonic interface
- **Beautiful Output**: Rich terminal formatting with tables and colors
- **Well Tested**: Comprehensive test suite with >80% coverage

## Installation

```bash
pip install helpspot
```

Or with development dependencies:

```bash
pip install helpspot[dev]
```

After installation, the `helpspot` command will be available in your terminal.

## Quick Start

### Python SDK

```python
from helpspot import HelpSpotClient

# Initialize the client with an API token (recommended)
client = HelpSpotClient(
    base_url="https://support.example.com",
    api_token="1|5VdNXJEtsPoFpX1KH5yc0BO2wlCqDp0sRTxZtox3"
)

# Create a request
request = client.requests.create(
    note="My printer is not working",
    category_id=2,
    email="user@example.com",
    first_name="John",
    last_name="Doe"
)
print(f"Created request #{request.x_request}")

# Get request details
request = client.requests.get(request_id=12345)
print(f"Status: {request.status}")
print(f"Category: {request.category}")

# Search requests
results = client.requests.search(
    query="printer",
    status_id=1,  # Active
    category_id=2,
    start=0,
    length=50
)
for req in results:
    print(f"#{req.x_request}: {req.title}")

# List user's filters
filters = client.filters.list()
for f in filters:
    print(f"{f.name}: {f.count} requests")

# Get filter results (e.g., inbox)
inbox = client.filters.get(filter_id="inbox")
for req in inbox:
    print(f"#{req.x_request}: {req.full_name}")
```

### Command-Line Interface

The `helpspot` CLI provides a convenient way to interact with HelpSpot from your terminal:

```bash
# Check API version
helpspot --base-url="https://support.example.com" version

# Create a ticket
helpspot --base-url="https://support.example.com" \
  --username="user@example.com" \
  --password="your_password" \
  tickets create \
    --note="Printer is not working" \
    --email="customer@example.com" \
    --first-name="John" \
    --last-name="Doe" \
    --title="Printer Issue" \
    --category-id=2

# List categories
helpspot --base-url="https://support.example.com" \
  categories list --active-only

# Get ticket details
helpspot --base-url="https://support.example.com" \
  --username="user@example.com" \
  --password="your_password" \
  tickets get 12345
```

**Environment Variables**: To avoid passing credentials on every command, set these environment variables:

```bash
export HELPSPOT_URL="https://support.example.com"
export HELPSPOT_USERNAME="user@example.com"
export HELPSPOT_PASSWORD="your_password"
# Or use an API token instead
export HELPSPOT_API_TOKEN="1|your_token_here"

# Now run commands without credentials
helpspot version
helpspot tickets create --note="Issue" --email="user@example.com" --title="Title" --category-id=2
```

**For self-signed certificates**, add the `--no-verify-ssl` flag:

```bash
helpspot --no-verify-ssl version
```

See the [CLI Documentation](CLI.md) for complete command reference.

## Authentication

### Python SDK

#### API Token (Recommended)

Generate an API token from your HelpSpot staff preferences:

```python
client = HelpSpotClient(
    base_url="https://support.example.com",
    api_token="1|your_token_here"
)
```

#### Basic Authentication

Use your HelpSpot username and password:

```python
client = HelpSpotClient(
    base_url="https://support.example.com",
    username="user@example.com",
    password="your_password"
)
```

#### Public API (No Authentication)

Some methods work without authentication:

```python
client = HelpSpotClient(base_url="https://support.example.com")

# Get request by access key
request = client.requests.get(access_key="12345abcxyz")

# List public categories
categories = client.categories.list()
```

### CLI

The CLI supports the same authentication methods via command-line options or environment variables:

**Command-line options:**
```bash
# API Token
helpspot --base-url="https://support.example.com" \
  --api-token="1|your_token_here" \
  tickets get 123

# Username and password
helpspot --base-url="https://support.example.com" \
  --username="user@example.com" \
  --password="your_password" \
  tickets get 123
```

**Environment variables (recommended):**
```bash
# Set once in your shell profile (~/.bashrc, ~/.zshrc, etc.)
export HELPSPOT_URL="https://support.example.com"
export HELPSPOT_API_TOKEN="1|your_token_here"
# Or use username/password
export HELPSPOT_USERNAME="user@example.com"
export HELPSPOT_PASSWORD="your_password"

# Then use commands without auth flags
helpspot tickets get 123
```

## Command-Line Interface

The HelpSpot CLI provides a rich command-line interface with beautiful table formatting powered by the Rich library.

### Available Commands

#### General Commands

```bash
# Show API version
helpspot version

# Show current configuration
helpspot config
```

#### Ticket Management

```bash
# Create a new ticket
helpspot tickets create \
  --note="Description of the issue" \
  --email="customer@example.com" \
  --first-name="John" \
  --last-name="Doe" \
  --title="Issue title" \
  --category-id=2 \
  [--urgent] \
  [--phone="555-1234"]

# Get ticket details
helpspot tickets get <request_id> [--raw-values]

# Search tickets
helpspot tickets search \
  --query="printer" \
  [--status-id=1] \
  [--category-id=2] \
  [--open] \
  [--limit=50]
```

#### Categories

```bash
# List all categories
helpspot categories list [--active-only]
```

#### Filters

```bash
# List all filters
helpspot filters list

# Get filter results (inbox, myq, or custom filter ID)
helpspot filters get <filter_id> [--limit=50]
```

### Global Options

All commands support these global options:

```bash
--base-url TEXT         HelpSpot base URL (or set HELPSPOT_URL)
--api-token TEXT        API token (or set HELPSPOT_API_TOKEN)
--username TEXT         Username for basic auth (or set HELPSPOT_USERNAME)
--password TEXT         Password for basic auth (or set HELPSPOT_PASSWORD)
--no-verify-ssl         Disable SSL certificate verification
--help                  Show help message
```

### Examples

**Create a ticket with environment variables:**
```bash
export HELPSPOT_URL="https://support.example.com"
export HELPSPOT_USERNAME="user@example.com"
export HELPSPOT_PASSWORD="password"

helpspot tickets create \
  --note="Server is down" \
  --email="admin@example.com" \
  --first-name="Admin" \
  --last-name="User" \
  --title="Server Outage" \
  --category-id=5 \
  --urgent
```

**List active categories:**
```bash
helpspot categories list --active-only
```

**Get your inbox:**
```bash
helpspot filters get inbox --limit=10
```

**Search for tickets:**
```bash
helpspot tickets search --query="database" --open --limit=25
```

For more CLI examples and detailed documentation, see [CLI.md](CLI.md).

## API Methods (Python SDK)

### Requests

```python
# Create a request
request = client.requests.create(
    note="Request description",
    category_id=1,
    email="customer@example.com",
    first_name="Jane",
    last_name="Smith",
    is_urgent=False,
    custom_fields={1: "value1", 2: "value2"},
    files=[{
        "filename": "screenshot.png",
        "mime_type": "image/png",
        "content": b"..."  # file bytes
    }]
)

# Get request (private API)
request = client.requests.get(request_id=123)

# Get request (public API)
request = client.requests.get(access_key="12345abcxyz")

# Update request
request = client.requests.update(
    request_id=123,
    note="Adding more information",
    status_id=2,
    is_urgent=True
)

# Search requests
results = client.requests.search(
    query="printer",
    status_id=1,
    category_id=2,
    is_open=True,
    assigned_to=5,
    start=0,
    length=50
)
```

### Customers

```python
# Get customer's requests (public API)
requests = client.customers.get_requests(
    email="customer@example.com",
    password="portal_password"
)
```

### Categories

```python
# List all categories
categories = client.categories.list()

for cat in categories:
    print(f"{cat.name} (ID: {cat.x_category})")
```

### Custom Fields

```python
# List all custom fields
fields = client.custom_fields.list()

# List custom fields for a specific category
fields = client.custom_fields.list(category_id=1)
```

### Filters

```python
# List user's filters
filters = client.filters.list()

# Get filter results
inbox = client.filters.get(filter_id="inbox", start=0, length=50)
my_queue = client.filters.get(filter_id="myq")
custom_filter = client.filters.get(filter_id="123")
```

### Status Types

```python
# List all active status types
statuses = client.status_types.list()

# List all status types (including inactive)
statuses = client.status_types.list(active_only=False)
```

### Version

```python
# Get API version information
version = client.version()
print(f"API version: {version.version}")
print(f"Min version: {version.min_version}")
```

## Error Handling

The library provides specific exceptions for different error cases:

```python
from helpspot import HelpSpotClient
from helpspot.exceptions import (
    APIError,
    AuthenticationError,
    AuthenticationRequiredError,
    APIDisabledError,
    ValidationError,
    HTTPError
)

client = HelpSpotClient(base_url="https://support.example.com")

try:
    # This will fail without authentication
    request = client.requests.search(query="test")
except AuthenticationRequiredError:
    print("This method requires authentication")

try:
    request = client.requests.get(request_id=99999)
except APIError as e:
    print(f"API Error {e.error_id}: {e.description}")
except HTTPError as e:
    print(f"HTTP Error: {e}")
```

## File Uploads

Upload files when creating or updating requests:

```python
from pathlib import Path

# Read file content
file_content = Path("screenshot.png").read_bytes()

# Create request with file attachment
request = client.requests.create(
    note="Screenshot attached",
    category_id=1,
    email="user@example.com",
    files=[
        {
            "filename": "screenshot.png",
            "mime_type": "image/png",
            "content": file_content
        }
    ]
)
```

## Context Manager

Use the client as a context manager for automatic cleanup:

```python
with HelpSpotClient(base_url="https://support.example.com", api_token="...") as client:
    request = client.requests.get(request_id=123)
    print(request.title)
# Client is automatically closed
```

## Configuration

### Timeout

Set a custom timeout for HTTP requests:

```python
client = HelpSpotClient(
    base_url="https://support.example.com",
    api_token="...",
    timeout=60.0  # seconds
)
```

### SSL Certificate Verification

By default, SSL certificates are verified. For self-signed certificates or testing environments, you can disable SSL verification:

```python
client = HelpSpotClient(
    base_url="https://support.example.com",
    api_token="...",
    verify_ssl=False  # Disable SSL verification (not recommended for production)
)
```

**Warning:** Disabling SSL verification is not recommended for production environments as it makes your connection vulnerable to man-in-the-middle attacks.

### Output Format

While the library defaults to JSON (recommended), you can specify other formats:

```python
client = HelpSpotClient(
    base_url="https://support.example.com",
    api_token="...",
    output_format="json"  # or "xml" or "php"
)
```

## Development

### Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/helpspot/helpspot-python.git
cd helpspot-python
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=helpspot --cov-report=html
```

### Type Checking

```bash
mypy src/helpspot
```

### Linting

```bash
ruff check src tests
```

## Requirements

### Core Dependencies
- Python 3.12+
- httpx >= 0.27.0
- pydantic >= 2.9.0

### CLI Dependencies
- click >= 8.3.1
- rich >= 14.3.1

All dependencies are automatically installed when you install the package.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [HelpSpot API Documentation](https://support.helpspot.com/index.php?pg=kb.chapter&id=28)
- [HelpSpot Website](https://www.helpspot.com/)
- [Issue Tracker](https://github.com/helpspot/helpspot-python/issues)

## Support

For issues with this library, please open an issue on GitHub.

For HelpSpot product support, contact [HelpSpot Support](https://helpspot.com/support).
