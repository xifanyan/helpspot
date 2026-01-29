# HelpSpot CLI

A powerful command-line interface for managing HelpSpot tickets, categories, filters, and more.

## Installation

The CLI is included with the HelpSpot Python package:

```bash
pip install helpspot
```

Or with `uv`:

```bash
uv pip install helpspot
```

## Quick Start

### Using Environment Variables (Recommended)

Set your HelpSpot credentials as environment variables:

```bash
export HELPSPOT_URL="https://your-helpspot.com"
export HELPSPOT_USERNAME="your-username"
export HELPSPOT_PASSWORD="your-password"
# OR use API token instead
export HELPSPOT_API_TOKEN="your-api-token"
```

Then use the CLI without typing credentials every time:

```bash
helpspot version
helpspot categories list --active-only
helpspot tickets create --note="Issue description" --email="user@example.com"
```

### Using Command-Line Options

You can also pass credentials directly:

```bash
helpspot --base-url="https://your-helpspot.com" \
         --username="user@example.com" \
         --password="yourpass" \
         version
```

### For Self-Signed Certificates

If your HelpSpot instance uses a self-signed SSL certificate:

```bash
helpspot --base-url="https://your-helpspot.com" \
         --username="user" \
         --password="pass" \
         --no-verify-ssl \
         version
```

## Commands

### General Commands

#### Show Version

```bash
helpspot version
```

#### Show Configuration

```bash
helpspot config
```

### Ticket Management

#### Create a Ticket

```bash
# Basic ticket
helpspot tickets create \
  --note="Printer not working" \
  --email="user@example.com" \
  --first-name="John" \
  --last-name="Doe" \
  --title="Printer Issue" \
  --category-id=33

# Urgent ticket
helpspot tickets create \
  --note="Server down!" \
  --email="admin@example.com" \
  --title="Critical Server Issue" \
  --category-id=33 \
  --urgent
```

#### Get Ticket Details

```bash
# Get ticket with text values
helpspot tickets get 12345

# Get ticket with raw IDs
helpspot tickets get 12345 --raw
```

#### Search Tickets

```bash
# Search by query
helpspot tickets search --query="printer"

# Search by email
helpspot tickets search --email="user@example.com"

# Search open tickets in a category
helpspot tickets search --category=33 --open-only --limit=50

# Search by status
helpspot tickets search --status=1 --limit=100
```

### Category Management

#### List Categories

```bash
# List all categories
helpspot categories list

# List only active categories
helpspot categories list --active-only
```

### Filter Management

#### List Filters

```bash
helpspot filters list
```

#### Get Filter Results

```bash
# Get inbox
helpspot filters get inbox --limit=25

# Get your queue
helpspot filters get myq

# Get custom filter by ID
helpspot filters get 42 --limit=50
```

## Options Reference

### Global Options

- `--base-url TEXT` - HelpSpot base URL (env: `HELPSPOT_URL`) **[required]**
- `--username TEXT` - Username for authentication (env: `HELPSPOT_USERNAME`)
- `--password TEXT` - Password for authentication (env: `HELPSPOT_PASSWORD`)
- `--api-token TEXT` - API token for authentication (env: `HELPSPOT_API_TOKEN`)
- `--no-verify-ssl` - Disable SSL certificate verification
- `--help` - Show help message

### Ticket Create Options

- `--note, -n TEXT` - Ticket description/note **[required]**
- `--email, -e TEXT` - Customer email **[required]**
- `--first-name, -f TEXT` - Customer first name
- `--last-name, -l TEXT` - Customer last name
- `--title, -t TEXT` - Ticket title/subject
- `--category-id, -c INTEGER` - Category ID
- `--urgent` - Mark as urgent

### Ticket Search Options

- `--query, -q TEXT` - Search query
- `--email, -e TEXT` - Customer email
- `--status, -s INTEGER` - Status ID
- `--category, -c INTEGER` - Category ID
- `--open-only` - Show only open tickets
- `--limit, -l INTEGER` - Number of results (default: 25)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HELPSPOT_URL` | HelpSpot base URL |
| `HELPSPOT_USERNAME` | Username for authentication |
| `HELPSPOT_PASSWORD` | Password for authentication |
| `HELPSPOT_API_TOKEN` | API token (alternative to username/password) |

## Examples

### Daily Workflow

```bash
# Set up environment (run once per session)
export HELPSPOT_URL="https://support.example.com"
export HELPSPOT_USERNAME="agent@example.com"
export HELPSPOT_PASSWORD="yourpassword"

# Check inbox
helpspot filters get inbox

# Search for printer issues
helpspot tickets search --query="printer" --open-only

# Get details of a specific ticket
helpspot tickets get 12345

# List all active categories
helpspot categories list --active-only

# Create a new ticket
helpspot tickets create \
  --note="Customer reports login issues" \
  --email="customer@example.com" \
  --first-name="Jane" \
  --last-name="Smith" \
  --title="Login Problem" \
  --category-id=33
```

### Automation Scripts

Create a shell script to automate common tasks:

```bash
#!/bin/bash
# check-urgent-tickets.sh

export HELPSPOT_URL="https://support.example.com"
export HELPSPOT_API_TOKEN="your-api-token"

echo "Checking urgent open tickets..."
helpspot tickets search --open-only --limit=100 | grep "!"
```

### Using with Cron

Schedule regular checks:

```bash
# Check inbox every 5 minutes
*/5 * * * * /usr/local/bin/helpspot filters get inbox --limit=10 >> /var/log/helpspot-inbox.log 2>&1
```

## Tips

1. **Use Environment Variables**: Set `HELPSPOT_*` variables in your shell profile (`.bashrc`, `.zshrc`) to avoid typing credentials every time.

2. **API Token vs Username/Password**: API tokens are more secure and recommended for CLI usage.

3. **Limit Results**: Use `--limit` to control the number of results returned in search and filter commands.

4. **Raw vs Text Values**: Use `--raw` flag with `tickets get` to see numeric IDs instead of text values (useful for scripting).

5. **Active Categories Only**: Use `--active-only` when listing categories to see only categories you can use.

## Troubleshooting

### Authentication Error

```
Error: Authentication required
```

**Solution**: Make sure you've set either:
- `HELPSPOT_USERNAME` and `HELPSPOT_PASSWORD`, OR
- `HELPSPOT_API_TOKEN`

### SSL Certificate Error

```
Error: SSL certificate verification failed
```

**Solution**: Use the `--no-verify-ssl` flag:

```bash
helpspot --no-verify-ssl version
```

### Command Not Found

```
helpspot: command not found
```

**Solution**: Make sure the package is installed and your PATH includes Python scripts:

```bash
pip install helpspot
# or
uv pip install helpspot
```

## Getting Help

For any command, use `--help`:

```bash
helpspot --help
helpspot tickets --help
helpspot tickets create --help
```

## Contributing

Report issues or contribute at: https://github.com/helpspot/helpspot-python
