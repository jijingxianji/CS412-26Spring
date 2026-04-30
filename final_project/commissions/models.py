from django.db import models


class Artist(models.Model):
    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    is_open_for_commissions = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CommissionPackage(models.Model):
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
        return f"{self.title} - {self.artist.display_name}"


class CommissionRequest(models.Model):
    class Status(models.TextChoices):
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
        return f"{self.request_title} ({self.status})"