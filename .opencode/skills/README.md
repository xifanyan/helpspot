# Spark OpenCode Skills

This directory contains OpenCode agent skills for working with the Spark (HelpSpot) support system.

## Available Skills

### 1. spark-categories
Lists all categories from Spark with filtering options.

**Usage:** "List all Spark categories" or "Show me active Spark categories"

### 2. spark-search  
Searches for Spark tickets using various criteria (email, status, category, query).

**Usage:** "Search Spark for tickets from user@example.com" or "Find urgent Spark tickets"

### 3. spark-ticket
Creates new Spark tickets and views existing ticket details.

**Usage:** "Create a Spark ticket for john@example.com" or "Show me Spark ticket #1234"

## Secure Credential Setup

**IMPORTANT: Never commit credentials to git.**

### Recommended: Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):

```bash
export HELPSPOT_URL="https://your-spark-instance.com"
export HELPSPOT_USERNAME="your-username"
export HELPSPOT_PASSWORD="your-password"
```

Then reload: `source ~/.bashrc`

### Alternative: Local .env File

Copy `.env.example` to `.env` and fill in your Spark credentials:

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

Load before using OpenCode:
```bash
source .env
```

Or use [direnv](https://direnv.net/) for automatic loading.

### Advanced: Password Managers

For team environments, use password manager CLIs:

- **1Password**: `export HELPSPOT_PASSWORD=$(op read "op://vault/spark/password")`
- **pass**: `export HELPSPOT_PASSWORD=$(pass spark/password)`
- **macOS Keychain**: `export HELPSPOT_PASSWORD=$(security find-generic-password -s spark -w)`

## SSL Certificate Issues

If you encounter SSL certificate errors, you can disable verification (not recommended for production):

```bash
# Add this to your .env or shell profile
export HELPSPOT_NO_VERIFY_SSL=1
```

Or use the `--no-verify-ssl` flag when calling the CLI directly.

## Security Best Practices

✅ **DO:**
- Store credentials in environment variables or password managers
- Use `.env` files for local development (already in `.gitignore`)
- Use API tokens instead of passwords when possible
- Rotate credentials regularly

❌ **DON'T:**
- Commit credentials to git
- Pass credentials as command-line arguments
- Share credentials in chat or documentation
- Use the same password across multiple services

## Getting Help

For more information, see:
- [OpenCode Skills Documentation](https://opencode.ai/docs/skills/)
- [Spark (HelpSpot) API Documentation](https://support.helpspot.com/index.php?pg=kb.page&id=164)
