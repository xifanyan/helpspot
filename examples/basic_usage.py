"""Basic usage example for HelpSpot Python client."""

from helpspot import HelpSpotClient

# Initialize the client
client = HelpSpotClient(
    base_url="https://zap.caseshare.com/spark",
    username="pyan@opentext.com",
    password="Cartman2024!",
    # api_token="1|your_api_token_here",  # Get this from staff preferences
    verify_ssl=False,  # Disable SSL verification for self-signed certificates
)

# Get API version
version = client.version()
print(f"API Version: {version.version}")
print(f"Minimum Version: {version.min_version}")
print()

# List categories
print("Available Categories:")
categories = client.categories.list()
for cat in categories:
    print(f"  - {cat.name} (ID: {cat.x_category})")
print()

# List filters
print("Your Filters:")
filters = client.filters.list()
for f in filters:
    print(f"  - {f.name}: {f.count} requests")
print()

# Get inbox
print("Inbox Requests:")
inbox_requests = client.filters.get(filter_id="inbox", length=5)
for req in inbox_requests:
    print(f"  #{req.x_request}: {req.full_name} - {req.note[:50]}...")
print()

# Search for requests
print("Searching for 'printer' requests:")
results = client.requests.search(query="printer", length=5)
for req in results:
    status = "OPEN" if req.is_open else "CLOSED"
    print(f"  #{req.x_request} [{status}]: {req.title or req.note[:40]}")
print()

# Get a specific request
request_id = 12345  # Replace with actual request ID
try:
    request = client.requests.get(request_id=request_id)
    print(f"Request #{request.x_request}:")
    print(f"  Status: {request.status}")
    print(f"  Category: {request.category}")
    print(f"  Customer: {request.full_name}")
    print(f"  Assigned to: {request.person_assigned_to}")
except Exception as e:
    print(f"Could not fetch request #{request_id}: {e}")
