---
name: spark-ticket
description: Create and view tickets in Spark (HelpSpot) support system
license: MIT
compatibility: opencode
metadata:
  audience: support-staff
  workflow: spark
---

## What I do

- Create new Spark support tickets
- View existing Spark ticket details
- Display ticket information in formatted tables
- Handle customer information and categorization

## When to use me

Use this skill when you need to:
- Create a new Spark support ticket
- View details of an existing Spark ticket
- Check Spark ticket status and assignment
- Review Spark ticket notes and history

## How I work

I use the Spark (HelpSpot) Python CLI with ticket commands:

### Create a ticket
```bash
uv run helpspot tickets create --note "Description" --email "user@example.com" [OPTIONS]
```

### View a ticket
```bash
uv run helpspot tickets get TICKET_ID
```

## Create Options

- `--note, -n` (required) - Ticket description/note
- `--email, -e` (required) - Customer email
- `--first-name, -f` - Customer first name
- `--last-name, -l` - Customer last name
- `--title, -t` - Ticket title/subject
- `--category-id, -c` - Category ID
- `--urgent` - Mark as urgent

## Get Options

- `--raw` - Show raw field values (IDs instead of names)

## Example usage

Ask me:
- "Create a Spark ticket for john@example.com about password reset"
- "Show me Spark ticket #1234"
- "Create an urgent Spark ticket in category 5"
- "Get details for Spark ticket 5678"

## Requirements

- Spark URL must be configured (HELPSPOT_URL)
- Creating tickets works with or without authentication
- Viewing tickets requires authentication

## Notes

- When creating tickets, the system returns the new ticket ID
- Ticket numbers are prefixed with 'x' in the API (xRequest)
- Categories can be found using the spark-categories skill
