"""
Views for the Art Commission Platform.

This file contains:
- the home page view
- list and detail views for artists, clients, packages, and requests
- create, update, and delete views for packages and requests
- filter/report pages for browsing packages and summarizing requests
"""

from django.db.models import Q, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Artist, Client, CommissionPackage, CommissionRequest


class HomeView(TemplateView):
    """Display the home page with summary counts and recent requests."""

    template_name = "project/home.html"

    def get_context_data(self, **kwargs):
        """
        Add summary values to the home page.

        This method provides:
        - total number of artists
        - total number of clients
        - total number of packages
        - total number of requests
        - five most recent commission requests
        """
        context = super().get_context_data(**kwargs)
        context["artist_count"] = Artist.objects.count()
        context["client_count"] = Client.objects.count()
        context["package_count"] = CommissionPackage.objects.count()
        context["request_count"] = CommissionRequest.objects.count()
        context["recent_requests"] = (
            CommissionRequest.objects.select_related("client", "package", "package__artist")
            .order_by("-created_at")[:5]
        )
        return context


class ArtistListView(ListView):
    """Display all artists in alphabetical order."""

    model = Artist
    template_name = "project/artist_list.html"
    context_object_name = "artists"
    queryset = Artist.objects.order_by("display_name")


class ArtistDetailView(DetailView):
    """Display one artist and all packages created by that artist."""

    model = Artist
    template_name = "project/artist_detail.html"
    context_object_name = "artist"

    def get_queryset(self):
        """
        Preload related packages for better performance.

        This avoids extra database queries when the template
        shows the artist's package list.
        """
        return Artist.objects.prefetch_related("packages").order_by("display_name")

    def get_context_data(self, **kwargs):
        """
        Add the selected artist's packages to the template context.

        Packages are sorted by price, then title.
        """
        context = super().get_context_data(**kwargs)
        context["packages"] = self.object.packages.all().order_by("base_price", "title")
        return context


class ClientListView(ListView):
    """Display all clients in alphabetical order."""

    model = Client
    template_name = "project/client_list.html"
    context_object_name = "clients"
    queryset = Client.objects.order_by("first_name", "last_name")


class ClientDetailView(DetailView):
    """Display one client and all requests submitted by that client."""

    model = Client
    template_name = "project/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        """
        Preload request, package, and artist data for one client.

        This helps the detail page display related records efficiently.
        """
        return Client.objects.prefetch_related("requests__package__artist").order_by(
            "first_name", "last_name"
        )

    def get_context_data(self, **kwargs):
        """
        Add the selected client's request history to the template context.

        Requests are shown with related package and artist data,
        ordered from newest to oldest.
        """
        context = super().get_context_data(**kwargs)
        context["requests"] = self.object.requests.select_related(
            "package", "package__artist"
        ).order_by("-created_at")
        return context


class PackageListView(ListView):
    """Display all commission packages."""

    model = CommissionPackage
    template_name = "project/package_list.html"
    context_object_name = "packages"

    def get_queryset(self):
        """
        Return all packages with artist data already joined.

        Packages are sorted by title.
        """
        return CommissionPackage.objects.select_related("artist").order_by("title")


class PackageDetailView(DetailView):
    """Display one commission package and any related requests."""

    model = CommissionPackage
    template_name = "project/package_detail.html"
    context_object_name = "package"

    def get_queryset(self):
        """
        Preload the artist and related request/client data.

        This helps the detail page show package metadata
        and related requests efficiently.
        """
        return CommissionPackage.objects.select_related("artist").prefetch_related("requests__client")

    def get_context_data(self, **kwargs):
        """
        Add requests related to the current package.

        Related requests are ordered from newest to oldest.
        """
        context = super().get_context_data(**kwargs)
        context["related_requests"] = self.object.requests.select_related("client").order_by("-created_at")
        return context


class PackageCreateView(CreateView):
    """Handle creation of a new commission package."""

    model = CommissionPackage
    fields = ["artist", "title", "description", "base_price", "turnaround_days", "is_active"]
    template_name = "project/object_form.html"
    success_url = reverse_lazy("project:package_list")
    extra_context = {
        "page_title": "Create commission package",
        "submit_label": "Save package",
        "back_url": reverse_lazy("project:package_list"),
    }


class PackageUpdateView(UpdateView):
    """Handle editing an existing commission package."""

    model = CommissionPackage
    fields = ["artist", "title", "description", "base_price", "turnaround_days", "is_active"]
    template_name = "project/object_form.html"
    success_url = reverse_lazy("project:package_list")
    extra_context = {
        "page_title": "Update commission package",
        "submit_label": "Update package",
        "back_url": reverse_lazy("project:package_list"),
    }


class PackageDeleteView(DeleteView):
    """Handle deletion of a commission package."""

    model = CommissionPackage
    template_name = "project/object_confirm_delete.html"
    success_url = reverse_lazy("project:package_list")
    extra_context = {
        "page_title": "Delete commission package",
        "back_url": reverse_lazy("project:package_list"),
    }


class RequestListView(ListView):
    """Display all commission requests from newest to oldest."""

    model = CommissionRequest
    template_name = "project/request_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        """
        Return requests with related client, package, and artist data.

        Sorting newest first makes the newest request appear on top.
        """
        return (
            CommissionRequest.objects.select_related("client", "package", "package__artist")
            .order_by("-created_at")
        )


class RequestDetailView(DetailView):
    """Display full details for a single commission request."""

    model = CommissionRequest
    template_name = "project/request_detail.html"
    context_object_name = "commission_request"

    def get_queryset(self):
        """
        Preload related foreign key data for one request.

        This prevents extra database lookups in the detail template.
        """
        return CommissionRequest.objects.select_related("client", "package", "package__artist")


class RequestCreateView(CreateView):
    """Handle creation of a new commission request."""

    model = CommissionRequest
    fields = [
        "client",
        "package",
        "request_title",
        "request_description",
        "reference_image_url",
        "deadline",
        "status",
    ]
    template_name = "project/object_form.html"
    success_url = reverse_lazy("project:request_list")
    extra_context = {
        "page_title": "Create commission request",
        "submit_label": "Save request",
        "back_url": reverse_lazy("project:request_list"),
    }


class RequestUpdateView(UpdateView):
    """Handle editing an existing commission request."""

    model = CommissionRequest
    fields = [
        "client",
        "package",
        "request_title",
        "request_description",
        "reference_image_url",
        "deadline",
        "status",
    ]
    template_name = "project/object_form.html"
    success_url = reverse_lazy("project:request_list")
    extra_context = {
        "page_title": "Update commission request",
        "submit_label": "Update request",
        "back_url": reverse_lazy("project:request_list"),
    }


class RequestDeleteView(DeleteView):
    """Handle deletion of a commission request."""

    model = CommissionRequest
    template_name = "project/object_confirm_delete.html"
    success_url = reverse_lazy("project:request_list")
    extra_context = {
        "page_title": "Delete commission request",
        "back_url": reverse_lazy("project:request_list"),
    }


def package_browse(request):
    """
    Filter and display commission packages.

    Supported filters:
    - q: keyword search across title, description, and artist name
    - artist: artist id
    - max_price: upper bound for package price
    - only_open: whether to show only artists currently open for commissions
    """
    packages = CommissionPackage.objects.select_related("artist").order_by("base_price", "title")
    artists = Artist.objects.order_by("display_name")

    q = request.GET.get("q", "").strip()
    artist_id = request.GET.get("artist", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    only_open = request.GET.get("only_open", "1")

    if q:
        packages = packages.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(artist__display_name__icontains=q)
        )

    if artist_id:
        packages = packages.filter(artist_id=artist_id)

    if max_price:
        packages = packages.filter(base_price__lte=max_price)

    if only_open == "1":
        packages = packages.filter(artist__is_open_for_commissions=True)

    context = {
        "packages": packages,
        "artists": artists,
        "q": q,
        "artist_id": artist_id,
        "max_price": max_price,
        "only_open": only_open,
    }
    return render(request, "project/package_browse.html", context)


def request_report(request):
    """
    Filter commission requests and build a status summary.

    Supported filters:
    - status: request status
    - artist: artist id through related package
    - client: client id

    The page also aggregates request counts by status.
    """
    requests_qs = (
        CommissionRequest.objects.select_related("client", "package", "package__artist")
        .order_by("-created_at")
    )

    status_filter = request.GET.get("status", "").strip()
    artist_id = request.GET.get("artist", "").strip()
    client_id = request.GET.get("client", "").strip()

    if status_filter:
        requests_qs = requests_qs.filter(status=status_filter)

    if artist_id:
        requests_qs = requests_qs.filter(package__artist_id=artist_id)

    if client_id:
        requests_qs = requests_qs.filter(client_id=client_id)

    status_counts = (
        requests_qs.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    context = {
        "requests": requests_qs,
        "status_counts": status_counts,
        "status_choices": CommissionRequest.Status.choices,
        "artists": Artist.objects.order_by("display_name"),
        "clients": Client.objects.order_by("first_name", "last_name"),
        "status_filter": status_filter,
        "artist_id": artist_id,
        "client_id": client_id,
    }
    return render(request, "project/request_report.html", context)