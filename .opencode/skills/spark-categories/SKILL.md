---
name: spark-categories
description: List all categories from Spark (HelpSpot) support system
license: MIT
compatibility: opencode
metadata:
  audience: support-staff
  workflow: spark
---

## What I do

- Connect to the Spark API using configured credentials
- Fetch all available categories from Spark
- Display categories in a formatted table with ID, name, status, and default assignee
- Support filtering to show only active categories

## When to use me

Use this skill when you need to:
- View all available Spark ticket categories
- Check category IDs for creating or updating tickets
- Verify which categories are active or deleted
- See default assignees for categories

## How I work

I use the Spark (HelpSpot) Python CLI that's already configured in this project. The skill will:

1. Check for Spark credentials in environment variables:
   - `HELPSPOT_URL` - Your Spark instance URL
   - `HELPSPOT_USERNAME` and `HELPSPOT_PASSWORD` - Basic auth credentials
   - OR `HELPSPOT_API_TOKEN` - API token authentication

2. Run the command: `uv run helpspot categories list`
   - Add `--no-verify-ssl` flag if SSL certificate issues occur

3. Display results in a formatted table showing:
   - Category ID (xCategory)
   - Category name
   - Status (Active/Deleted)
   - Default person assigned

## Secure credential setup

**NEVER commit credentials to git.** Use one of these secure methods:

### Option 1: Shell environment (recommended for personal use)
Add to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:
```bash
export HELPSPOT_URL="https://your-spark-instance.com"
export HELPSPOT_USERNAME="your-username"
export HELPSPOT_PASSWORD="your-password"
```

### Option 2: Local .env file (already in .gitignore)
Create `.env` in project root:
```bash
HELPSPOT_URL=https://your-spark-instance.com
HELPSPOT_USERNAME=your-username
HELPSPOT_PASSWORD=your-password
```

Then load it before using OpenCode:
```bash
source .env  # or use direnv for automatic loading
```

### Option 3: Password managers
Use tools like:
- **1Password CLI**: `op read "op://vault/spark/password"`
- **pass**: `pass spark/password`
- **keychain** (macOS): `security find-generic-password -s spark -w`

See `.env.example` for a template.

## Options

- `--active-only` - Show only active categories (exclude deleted ones)

## Example usage

Ask me:
- "List all Spark categories"
- "Show me the active Spark categories"
- "What Spark category IDs are available?"
- "Which Spark categories are assigned to person 5?"

## Requirements

- Spark URL must be configured (HELPSPOT_URL environment variable)
- Authentication is optional but recommended for private categories
- The `helpspot` CLI tool must be available (installed via uv)
- If SSL certificate errors occur, use `--no-verify-ssl` flag (not recommended for production)

## Error handling

If credentials are missing, I'll help you set them up securely. If the API is unreachable, I'll provide troubleshooting steps.

## Security notes

- Credentials are read from environment variables only
- Never pass credentials as command-line arguments (visible in process list)
- Never commit `.env` file (already in .gitignore)
- Use password managers for team environments
- Consider using API tokens instead of passwords when possible
