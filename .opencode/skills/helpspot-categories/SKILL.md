---
name: helpspot-categories
description: List all categories from HelpSpot support system
license: MIT
compatibility: opencode
metadata:
  audience: support-staff
  workflow: helpspot
---

## What I do

- Connect to the HelpSpot API using configured credentials
- Fetch all available categories from HelpSpot
- Display categories in a formatted table with ID, name, status, and default assignee
- Support filtering to show only active categories

## When to use me

Use this skill when you need to:
- View all available support ticket categories
- Check category IDs for creating or updating tickets
- Verify which categories are active or deleted
- See default assignees for categories

## How I work

I use the HelpSpot Python CLI that's already configured in this project. The skill will:

1. Check for HelpSpot credentials in environment variables:
   - `HELPSPOT_URL` - Your HelpSpot base URL
   - `HELPSPOT_USERNAME` and `HELPSPOT_PASSWORD` - Basic auth credentials
   - OR `HELPSPOT_API_TOKEN` - API token authentication

2. Run the command: `uv run helpspot categories list`

3. Display results in a formatted table showing:
   - Category ID (xCategory)
   - Category name
   - Status (Active/Deleted)
   - Default person assigned

## Options

- `--active-only` - Show only active categories (exclude deleted ones)

## Example usage

Ask me:
- "List all HelpSpot categories"
- "Show me the active categories"
- "What category IDs are available?"
- "Which categories are assigned to person 5?"

## Requirements

- HelpSpot URL must be configured (HELPSPOT_URL environment variable)
- Authentication is optional but recommended for private categories
- The `helpspot` CLI tool must be available (installed via uv)

## Error handling

If credentials are missing, I'll prompt you to set them up. If the API is unreachable, I'll provide troubleshooting steps.
