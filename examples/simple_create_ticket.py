"""Simple example of creating a ticket using HelpSpot Python client."""

from helpspot import HelpSpotClient

# Initialize the client
client = HelpSpotClient(
    base_url="https://zap.caseshare.com/spark",
    username="pyan@opentext.com",
    password="Cartman2024!",
    verify_ssl=False,  # For self-signed certificates
    timeout=60.0,
)

print("Creating a HelpSpot ticket...")
print("-" * 50)

# Create a new ticket
ticket = client.requests.create(
    note="This is a test ticket created using the HelpSpot Python client library.",
    email="pyan@opentext.com",
    first_name="Paul",
    last_name="Yan",
    title="Test Ticket from Python API",
    category_id=1,
    is_urgent=False,
)

print(f"Success! Created ticket #{ticket.x_request}")
print()

# Retrieve the ticket with raw values (gets IDs instead of names)
print("Retrieving ticket details...")
details = client.requests.get(request_id=ticket.x_request, raw_values=True)

print(f"  Ticket ID: {details.x_request}")
print(f"  Title: {details.title}")
print(f"  Email: {details.email}")
print(f"  Name: {details.full_name}")
print(f"  Status ID: {details.status}")
print(f"  Category ID: {details.category}")

# Close the client
client.close()
print()
print("-" * 50)
print("Done!")
