"""
Seed script for the Art Commission Platform.

This script clears old demo data and recreates a small set of:
- artists
- clients
- commission packages
- commission requests

It is meant for testing and demonstration.
"""

from datetime import date
from project.models import Artist, Client, CommissionPackage, CommissionRequest

# Delete old demo data so the script can be run multiple times safely.
CommissionRequest.objects.all().delete()
CommissionPackage.objects.all().delete()
Client.objects.all().delete()
Artist.objects.all().delete()

# Create demo artists.
sky = Artist.objects.create(
    display_name="sky",
    email="sky@gmail.com",
    bio="Soft pastel artist.",
    profile_image_url="",
    is_open_for_commissions=True,
)

lemon = Artist.objects.create(
    display_name="lemon",
    email="lemon@gmail.com",
    bio="Cute bright icon artist.",
    profile_image_url="",
    is_open_for_commissions=True,
)

violet = Artist.objects.create(
    display_name="violet",
    email="violet@gmail.com",
    bio="Fantasy character designer.",
    profile_image_url="",
    is_open_for_commissions=True,
)

pinky = Artist.objects.create(
    display_name="pinky",
    email="pinky@gmail.com",
    bio="Chibi and couple illustration artist.",
    profile_image_url="",
    is_open_for_commissions=True,
)

# Create demo clients.
alice = Client.objects.create(
    first_name="Alice",
    last_name="Liu",
    email="alice@gmail.com",
    bio="Loves fantasy OCs.",
)

brian = Client.objects.create(
    first_name="Brian",
    last_name="Li",
    email="brian@gmail.com",
    bio="Looking for profile art.",
)

cindy = Client.objects.create(
    first_name="Cindy",
    last_name="Wang",
    email="cindy@gmail.com",
    bio="Wants cute chibi art.",
)

david = Client.objects.create(
    first_name="David",
    last_name="Xu",
    email="david@gmail.com",
    bio="Needs social media icons.",
)

# Create demo packages.
pkg1 = CommissionPackage.objects.create(
    artist=sky,
    title="Chibi Portrait",
    description="Simple chibi portrait with pastel colors.",
    base_price="100.00",
    turnaround_days=10,
    is_active=True,
)

pkg2 = CommissionPackage.objects.create(
    artist=lemon,
    title="Half-body Illustration",
    description="Half-body commission with clean coloring.",
    base_price="500.00",
    turnaround_days=30,
    is_active=True,
)

pkg3 = CommissionPackage.objects.create(
    artist=violet,
    title="Full Character Design",
    description="Detailed fantasy character design sheet.",
    base_price="1200.00",
    turnaround_days=45,
    is_active=True,
)

pkg4 = CommissionPackage.objects.create(
    artist=pinky,
    title="Couple Icon Set",
    description="Matching icon set for two characters.",
    base_price="100.00",
    turnaround_days=10,
    is_active=True,
)

# Create demo requests.
CommissionRequest.objects.create(
    client=cindy,
    package=pkg1,
    request_title="chibi chibi test",
    request_description="A cute pink chibi portrait.",
    reference_image_url="",
    deadline=date(2026, 5, 14),
    status="in_progress",
)

CommissionRequest.objects.create(
    client=alice,
    package=pkg3,
    request_title="character design test",
    request_description="A fantasy mage original character.",
    reference_image_url="",
    deadline=date(2026, 6, 16),
    status="accepted",
)

CommissionRequest.objects.create(
    client=brian,
    package=pkg2,
    request_title="half-body illustration test",
    request_description="Half-body art for a profile image.",
    reference_image_url="",
    deadline=date(2026, 8, 31),
    status="submitted",
)

CommissionRequest.objects.create(
    client=david,
    package=pkg4,
    request_title="icon set test",
    request_description="Matching icons for two friends.",
    reference_image_url="",
    deadline=date(2026, 5, 31),
    status="submitted",
)

# Print counts so the user can confirm the seed ran successfully.
print("Seed data created.")
print("Artists:", Artist.objects.count())
print("Clients:", Client.objects.count())
print("Packages:", CommissionPackage.objects.count())
print("Requests:", CommissionRequest.objects.count())