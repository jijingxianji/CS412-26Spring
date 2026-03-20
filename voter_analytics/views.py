"""
views.py for voter_analytics app.
Yanting Lyu, jixian77@bu.edu
"""

import datetime

from django.views.generic import ListView, DetailView
from .models import Voter


class VoterListView(ListView):
    """Display a paginated list of voters, with optional filtering."""

    model = Voter
    template_name = "voter_analytics/voter_list.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """Return the filtered queryset of voters."""
        qs = Voter.objects.all().order_by("last_name", "first_name")

        party = self.request.GET.get("party")
        min_year = self.request.GET.get("min_year")
        max_year = self.request.GET.get("max_year")
        voter_score = self.request.GET.get("voter_score")

        v20state = self.request.GET.get("v20state")
        v21town = self.request.GET.get("v21town")
        v21primary = self.request.GET.get("v21primary")
        v22general = self.request.GET.get("v22general")
        v23town = self.request.GET.get("v23town")

        if party:
            qs = qs.filter(party_affiliation=party)

        if min_year:
            qs = qs.filter(date_of_birth__year__gte=min_year)

        if max_year:
            qs = qs.filter(date_of_birth__year__lte=max_year)

        if voter_score:
            qs = qs.filter(voter_score=voter_score)

        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        """Add filter options and selected values to the template context."""
        context = super().get_context_data(**kwargs)

        context["party_choices"] = (
            Voter.objects.order_by("party_affiliation")
            .values_list("party_affiliation", flat=True)
            .distinct()
        )

        current_year = datetime.date.today().year
        context["year_choices"] = range(current_year, 1900, -1)
        context["score_choices"] = range(0, 6)

        context["selected_party"] = self.request.GET.get("party", "")
        context["selected_min_year"] = self.request.GET.get("min_year", "")
        context["selected_max_year"] = self.request.GET.get("max_year", "")
        context["selected_score"] = self.request.GET.get("voter_score", "")

        context["checked_v20state"] = self.request.GET.get("v20state", "")
        context["checked_v21town"] = self.request.GET.get("v21town", "")
        context["checked_v21primary"] = self.request.GET.get("v21primary", "")
        context["checked_v22general"] = self.request.GET.get("v22general", "")
        context["checked_v23town"] = self.request.GET.get("v23town", "")

        return context


class VoterDetailView(DetailView):
    """Display details for a single voter."""

    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        """Add a Google Maps query string for the voter address."""
        context = super().get_context_data(**kwargs)
        voter = self.get_object()

        address = f"{voter.street_address()}, Newton, MA {voter.zip_code}"
        context["google_maps_query"] = address.replace(" ", "+")
        return context


class GraphListView(ListView):
    """Placeholder for Task 3 graphs page."""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self):
        return Voter.objects.all()[:10]