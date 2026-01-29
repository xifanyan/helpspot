"""Example: List all HelpSpot categories and create a ticket."""

from helpspot import HelpSpotClient

# Initialize the client
client = HelpSpotClient(
    base_url="https://zap.caseshare.com/spark",
    username="pyan@opentext.com",
    password="Cartman2024!",
    verify_ssl=False,
    timeout=60.0,
)

print("=" * 60)
print("HelpSpot Categories Example")
print("=" * 60)
print()

# Load all categories
print("Loading categories...")
categories = client.categories.list()

print(f"Total categories: {len(categories)}")
print()

# Filter active categories only
active_categories = [cat for cat in categories if not cat.is_deleted]
print(f"Active categories: {len(active_categories)}")
print()

# Display active categories
print("Active Categories:")
print("-" * 60)
for cat in active_categories:
    default_person = f" (Default: {cat.default_person})" if cat.default_person else ""
    print(f"  {cat.x_category:3} - {cat.name}{default_person}")

print()
print("-" * 60)

# Create a ticket in a specific category
print()
print("Creating a ticket in 'Client Services - Enterprise Tech' category...")

# Find the category ID
cs_et_category = next((c for c in active_categories if "Enterprise Tech" in c.name), None)

if cs_et_category:
    ticket = client.requests.create(
        note="Example ticket created by the HelpSpot Python client library.",
        email="pyan@opentext.com",
        first_name="Paul",
        last_name="Yan",
        title="Test Ticket - Category Example",
        category_id=cs_et_category.x_category,
    )

    print(f"Success! Created ticket #{ticket.x_request} in category '{cs_et_category.name}'")
else:
    print("Category not found")

# Close the client
client.close()
print()
print("=" * 60)
print("Done!")
