#!/usr/bin/env python3
"""Setup script for HelpSpot CLI configuration."""

import os
import sys
from pathlib import Path


def main():
    """Interactive setup for HelpSpot CLI."""
    print("=" * 60)
    print("HelpSpot CLI Configuration Setup")
    print("=" * 60)
    print()

    # Get configuration
    base_url = input("HelpSpot base URL (e.g., https://support.example.com): ").strip()

    print()
    print("Choose authentication method:")
    print("1. Username and Password")
    print("2. API Token")
    choice = input("Enter choice (1 or 2): ").strip()

    username = ""
    password = ""
    api_token = ""

    if choice == "1":
        username = input("Username: ").strip()
        password = input("Password: ").strip()
    elif choice == "2":
        api_token = input("API Token: ").strip()
    else:
        print("Invalid choice!")
        sys.exit(1)

    verify_ssl = input("Verify SSL certificates? (yes/no) [yes]: ").strip().lower()
    verify_ssl = verify_ssl != "no"

    # Generate shell configuration
    print()
    print("=" * 60)
    print("Configuration")
    print("=" * 60)
    print()
    print("Add these lines to your shell profile (~/.bashrc or ~/.zshrc):")
    print()
    print(f'export HELPSPOT_URL="{base_url}"')

    if username:
        print(f'export HELPSPOT_USERNAME="{username}"')
        print(f'export HELPSPOT_PASSWORD="{password}"')
    else:
        print(f'export HELPSPOT_API_TOKEN="{api_token}"')

    print()
    print("Then reload your shell:")
    print("  source ~/.bashrc  # or source ~/.zshrc")
    print()
    print("Test the configuration:")

    no_verify = "" if verify_ssl else " --no-verify-ssl"
    print(f"  helpspot{no_verify} version")
    print()

    # Optionally write to file
    save = input("Save to helpspot.env file? (yes/no) [yes]: ").strip().lower()

    if save != "no":
        with open("helpspot.env", "w") as f:
            f.write(f"# HelpSpot CLI Configuration\n")
            f.write(f"# Source this file: source helpspot.env\n\n")
            f.write(f'export HELPSPOT_URL="{base_url}"\n')

            if username:
                f.write(f'export HELPSPOT_USERNAME="{username}"\n')
                f.write(f'export HELPSPOT_PASSWORD="{password}"\n')
            else:
                f.write(f'export HELPSPOT_API_TOKEN="{api_token}"\n')

        print()
        print("✓ Configuration saved to helpspot.env")
        print()
        print("To use this configuration:")
        print("  source helpspot.env")
        print(f"  helpspot{no_verify} version")

    print()
    print("=" * 60)
    print("Setup complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
