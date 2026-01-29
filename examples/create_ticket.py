"""Example of creating a ticket (request) in HelpSpot."""

from helpspot import HelpSpotClient
from helpspot.exceptions import APIError, HTTPError

# Initialize the client
client = HelpSpotClient(
    base_url="https://zap.caseshare.com/spark",
    username="pyan@opentext.com",
    password="Cartman2024!",
    verify_ssl=False,  # Disable SSL verification for self-signed certificates
    timeout=60.0,
)

print("HelpSpot Ticket Creation Example")
print("=" * 50)

try:
    # Get API version
    version = client.version()
    print(f"[OK] Connected to HelpSpot API v{version.version}")
    print()

    # Create a new ticket (request)
    # Note: In HelpSpot, tickets are called "requests"
    print("Creating a new ticket...")

    new_request = client.requests.create(
        note="This is a test ticket created using the HelpSpot Python client library. "
        "The library provides a modern, type-safe interface to the HelpSpot API.",
        email="pyan@opentext.com",
        first_name="Paul",
        last_name="Yan",
        title="Test Ticket from Python Client",  # Optional subject/title
        category_id=1,  # Use a valid category ID from your HelpSpot instance
        is_urgent=False,  # Set to True for urgent tickets
    )

    print(f"[OK] Successfully created ticket!")
    print(f"  Request ID: {new_request.x_request}")
    print(f"  Access Key: {new_request.access_key}")
    print(f"  Customer: {new_request.full_name}")
    print(f"  Email: {new_request.email}")
    print()

    # You can also retrieve the ticket details
    print("Retrieving ticket details...")
    retrieved = client.requests.get(request_id=new_request.x_request)
    print(f"[OK] Retrieved ticket #{retrieved.x_request}")
    print(f"  Status: {retrieved.status}")
    print(f"  Opened: {retrieved.opened_date or 'N/A'}")
    if retrieved.note:
        print(f"  Note: {retrieved.note[:100]}...")
    else:
        print(f"  Note: (no note available)")

except APIError as e:
    print(f"[ERROR] API Error {e.error_id}: {e.description}")
    print(f"  Details: {e}")
except HTTPError as e:
    print(f"[ERROR] HTTP Error: {e}")
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
finally:
    client.close()

print()
print("=" * 50)
print("Example completed!")
