"""HelpSpot CLI - Command-line interface for HelpSpot API."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from helpspot import HelpSpotClient
from helpspot.exceptions import APIError, HTTPError, AuthenticationRequiredError

console = Console()


def get_client(
    base_url: str,
    username: str | None,
    password: str | None,
    api_token: str | None,
    verify_ssl: bool,
) -> HelpSpotClient:
    """Create and return a HelpSpot client."""
    try:
        if api_token:
            client = HelpSpotClient(
                base_url=base_url,
                api_token=api_token,
                verify_ssl=verify_ssl,
                timeout=60.0,
            )
        elif username and password:
            client = HelpSpotClient(
                base_url=base_url,
                username=username,
                password=password,
                verify_ssl=verify_ssl,
                timeout=60.0,
            )
        else:
            client = HelpSpotClient(
                base_url=base_url,
                verify_ssl=verify_ssl,
                timeout=60.0,
            )
        return client
    except Exception as e:
        console.print(f"[red]Error creating client: {e}[/red]")
        sys.exit(1)


@click.group()
@click.option(
    "--base-url", envvar="HELPSPOT_URL", required=True, help="HelpSpot base URL (env: HELPSPOT_URL)"
)
@click.option(
    "--username",
    envvar="HELPSPOT_USERNAME",
    help="Username for authentication (env: HELPSPOT_USERNAME)",
)
@click.option(
    "--password",
    envvar="HELPSPOT_PASSWORD",
    help="Password for authentication (env: HELPSPOT_PASSWORD)",
)
@click.option(
    "--api-token",
    envvar="HELPSPOT_API_TOKEN",
    help="API token for authentication (env: HELPSPOT_API_TOKEN)",
)
@click.option(
    "--no-verify-ssl", is_flag=True, default=False, help="Disable SSL certificate verification"
)
@click.pass_context
def cli(ctx, base_url, username, password, api_token, no_verify_ssl):
    """HelpSpot CLI - Manage tickets, categories, and more."""
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["api_token"] = api_token
    ctx.obj["verify_ssl"] = not no_verify_ssl


@cli.command()
@click.pass_context
def version(ctx):
    """Show HelpSpot API version."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        ver = client.version()
        console.print(
            Panel(
                f"[cyan]API Version:[/cyan] {ver.version}\n"
                f"[cyan]Minimum Version:[/cyan] {ver.min_version}",
                title="HelpSpot Version",
                border_style="green",
            )
        )
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@cli.group()
def tickets():
    """Manage tickets (requests)."""
    pass


@tickets.command("create")
@click.option("--note", "-n", required=True, help="Ticket description/note")
@click.option("--email", "-e", required=True, help="Customer email")
@click.option("--first-name", "-f", help="Customer first name")
@click.option("--last-name", "-l", help="Customer last name")
@click.option("--title", "-t", help="Ticket title/subject")
@click.option("--category-id", "-c", type=int, help="Category ID")
@click.option("--urgent", is_flag=True, help="Mark as urgent")
@click.pass_context
def create_ticket(ctx, note, email, first_name, last_name, title, category_id, urgent):
    """Create a new ticket."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        with console.status("[bold green]Creating ticket..."):
            ticket = client.requests.create(
                note=note,
                email=email,
                first_name=first_name,
                last_name=last_name,
                title=title,
                category_id=category_id,
                is_urgent=urgent,
            )

        console.print(
            Panel(
                f"[green]Successfully created ticket![/green]\n\n"
                f"[cyan]Request ID:[/cyan] {ticket.x_request}\n"
                f"[cyan]Email:[/cyan] {email}\n"
                f"[cyan]Title:[/cyan] {title or 'N/A'}",
                title=f"Ticket #{ticket.x_request}",
                border_style="green",
            )
        )
    except APIError as e:
        console.print(f"[red]API Error {e.error_id}: {e.description}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@tickets.command("get")
@click.argument("ticket_id", type=int)
@click.option("--raw", is_flag=True, help="Show raw field values (IDs instead of names)")
@click.pass_context
def get_ticket(ctx, ticket_id, raw):
    """Get ticket details by ID."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        with console.status(f"[bold green]Fetching ticket #{ticket_id}..."):
            ticket = client.requests.get(request_id=ticket_id, raw_values=raw)

        table = Table(title=f"Ticket #{ticket.x_request}", box=box.ROUNDED)
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        table.add_row("ID", str(ticket.x_request))
        table.add_row("Title", ticket.title or "N/A")
        table.add_row("Email", ticket.email or "N/A")
        table.add_row("Name", ticket.full_name or "N/A")
        table.add_row("Status", str(ticket.status) or "N/A")
        table.add_row("Category", str(ticket.category) or "N/A")
        table.add_row("Opened By", ticket.person_opened_by or "N/A")
        table.add_row("Assigned To", ticket.person_assigned_to or "N/A")
        table.add_row("Urgent", "Yes" if ticket.is_urgent else "No")
        table.add_row("Open", "Yes" if ticket.is_open else "No")

        console.print(table)

        if ticket.note:
            console.print(
                Panel(
                    ticket.note[:500] + ("..." if len(ticket.note) > 500 else ""),
                    title="Latest Note",
                    border_style="blue",
                )
            )
    except APIError as e:
        console.print(f"[red]API Error {e.error_id}: {e.description}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@tickets.command("search")
@click.option("--query", "-q", help="Search query")
@click.option("--email", "-e", help="Customer email")
@click.option("--status", "-s", type=int, help="Status ID")
@click.option("--category", "-c", type=int, help="Category ID")
@click.option("--open-only", is_flag=True, help="Show only open tickets")
@click.option("--limit", "-l", type=int, default=25, help="Number of results (default: 25)")
@click.pass_context
def search_tickets(ctx, query, email, status, category, open_only, limit):
    """Search for tickets."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        with console.status("[bold green]Searching tickets..."):
            results = client.requests.search(
                query=query,
                email=email,
                status_id=status,
                category_id=category,
                is_open=open_only if open_only else None,
                length=limit,
            )

        if not results:
            console.print("[yellow]No tickets found.[/yellow]")
            return

        table = Table(title=f"Search Results ({len(results)} tickets)", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Customer", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Urgent", style="red")

        for ticket in results:
            table.add_row(
                str(ticket.x_request),
                (ticket.title or ticket.note[:40] if ticket.note else "N/A")[:40],
                ticket.full_name or ticket.email or "N/A",
                "OPEN" if ticket.is_open else "CLOSED",
                "!" if ticket.is_urgent else "",
            )

        console.print(table)
    except AuthenticationRequiredError:
        console.print("[red]Authentication required for search. Please provide credentials.[/red]")
    except APIError as e:
        console.print(f"[red]API Error {e.error_id}: {e.description}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@cli.group()
def categories():
    """Manage categories."""
    pass


@categories.command("list")
@click.option("--active-only", is_flag=True, help="Show only active categories")
@click.pass_context
def list_categories(ctx, active_only):
    """List all categories."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        with console.status("[bold green]Loading categories..."):
            cats = client.categories.list()

        if active_only:
            cats = [c for c in cats if not c.is_deleted]

        table = Table(title=f"Categories ({len(cats)} total)", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Status", style="green")
        table.add_column("Default Person", style="yellow")

        for cat in cats:
            table.add_row(
                str(cat.x_category),
                cat.name,
                "Active" if not cat.is_deleted else "Deleted",
                str(cat.default_person) if cat.default_person else "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@cli.group()
def filters():
    """Manage filters."""
    pass


@filters.command("list")
@click.pass_context
def list_filters(ctx):
    """List all filters."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        with console.status("[bold green]Loading filters..."):
            flts = client.filters.list()

        table = Table(title=f"Filters ({len(flts)} total)", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Type", style="green")
        table.add_column("Count", style="yellow")

        for flt in flts:
            table.add_row(
                str(flt.x_filter),
                flt.name,
                flt.filter_type or "N/A",
                str(flt.count) if flt.count else "0",
            )

        console.print(table)
    except AuthenticationRequiredError:
        console.print("[red]Authentication required. Please provide credentials.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@filters.command("get")
@click.argument("filter_id")
@click.option("--limit", "-l", type=int, default=25, help="Number of results (default: 25)")
@click.pass_context
def get_filter(ctx, filter_id, limit):
    """Get tickets from a filter (e.g., inbox, myq, or filter ID)."""
    client = get_client(
        ctx.obj["base_url"],
        ctx.obj["username"],
        ctx.obj["password"],
        ctx.obj["api_token"],
        ctx.obj["verify_ssl"],
    )

    try:
        with console.status(f"[bold green]Loading filter '{filter_id}'..."):
            results = client.filters.get(filter_id=filter_id, length=limit)

        if not results:
            console.print(f"[yellow]No tickets in filter '{filter_id}'.[/yellow]")
            return

        table = Table(title=f"Filter: {filter_id} ({len(results)} tickets)", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Customer", style="green")
        table.add_column("Status", style="yellow")

        for ticket in results:
            table.add_row(
                str(ticket.x_request),
                (ticket.title or ticket.note[:40] if ticket.note else "N/A")[:40],
                ticket.full_name or ticket.email or "N/A",
                "OPEN" if ticket.is_open else "CLOSED",
            )

        console.print(table)
    except AuthenticationRequiredError:
        console.print("[red]Authentication required. Please provide credentials.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        client.close()


@cli.command()
@click.pass_context
def config(ctx):
    """Show current configuration."""
    table = Table(title="HelpSpot CLI Configuration", box=box.ROUNDED)
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Base URL", ctx.obj["base_url"])
    table.add_row("Username", ctx.obj["username"] or "Not set")
    table.add_row("API Token", "Set" if ctx.obj["api_token"] else "Not set")
    table.add_row("SSL Verification", "Enabled" if ctx.obj["verify_ssl"] else "Disabled")

    console.print(table)
    console.print("\n[yellow]Tip:[/yellow] Set environment variables to avoid typing credentials:")
    console.print("  export HELPSPOT_URL='https://your-helpspot.com'")
    console.print("  export HELPSPOT_USERNAME='your-username'")
    console.print("  export HELPSPOT_PASSWORD='your-password'")
    console.print("  # OR")
    console.print("  export HELPSPOT_API_TOKEN='your-api-token'")


if __name__ == "__main__":
    cli(obj={})
