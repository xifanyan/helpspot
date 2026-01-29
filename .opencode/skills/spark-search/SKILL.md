---
name: spark-search
description: Search for tickets in Spark (HelpSpot) support system
license: MIT
compatibility: opencode
metadata:
  audience: support-staff
  workflow: spark
---

## What I do

- Search for Spark support tickets using various criteria
- Filter by email, status, category, or search query
- Display results in a formatted table
- Show ticket ID, title, customer, status, and urgency

## When to use me

Use this skill when you need to:
- Find Spark tickets for a specific customer email
- Search tickets by keyword or phrase
- Filter tickets by status or category
- Find urgent or open tickets

## How I work

I use the Spark (HelpSpot) Python CLI with the search command:

```bash
uv run helpspot tickets search [OPTIONS]
```

## Options

- `--query, -q` - Search query text
- `--email, -e` - Customer email address
- `--status, -s` - Status ID to filter by
- `--category, -c` - Category ID to filter by
- `--open-only` - Show only open tickets
- `--limit, -l` - Number of results (default: 25)

## Example usage

Ask me:
- "Search Spark for tickets from user@example.com"
- "Find all urgent Spark tickets"
- "Show open Spark tickets in category 5"
- "Search Spark for tickets about 'password reset'"

## Requirements

- Spark URL must be configured (HELPSPOT_URL)
- Authentication required (username/password or API token)
- Search requires private API access

## Notes

The search results are limited to 25 by default. You can increase this with the `--limit` option.
