"""
Data models for the Art Commission Platform.

This app stores four main entities:
1. Artist: a creator who offers commission work.
2. Client: a user who submits commission requests.
3. CommissionPackage: a package offered by an artist.
4. CommissionRequest: a request submitted by a client for a package.
"""

from django.db import models


class Artist(models.Model):
    """Represents an artist who can offer commission packages."""

    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    is_open_for_commissions = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the artist name for admin pages and dropdown lists."""
        return self.display_name


class Client(models.Model):
    """Represents a client who can submit commission requests."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the client's full name."""
        return f"{self.first_name} {self.last_name}"


class CommissionPackage(models.Model):
    """Represents a commission package created by an artist."""

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="packages"
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    turnaround_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable label combining package title and artist."""
        return f"{self.title} - {self.artist.display_name}"


class CommissionRequest(models.Model):
    """Represents a request submitted by a client for a package."""

    class Status(models.TextChoices):
        """Possible status values for a commission request."""

        SUBMITTED = "submitted", "Submitted"
        ACCEPTED = "accepted", "Accepted"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    package = models.ForeignKey(
        CommissionPackage,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    request_title = models.CharField(max_length=120)
    request_description = models.TextField()
    reference_image_url = models.URLField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable label for this request and its status."""
        return f"{self.request_title} ({self.status})"