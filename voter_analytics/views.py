"""
views.py for voter_analytics app.
Yanting Lyu, jixian77@bu.edu
"""

import datetime

from django.db.models import Count
from django.views.generic import ListView, DetailView
from plotly.offline import plot
import plotly.graph_objs as go

from .models import Voter


class VoterFilterMixin:
    """Shared filtering logic for list and graph views."""

    def get_filtered_queryset(self):
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

    def add_filter_context(self, context):
        """Add filter choices and selected values to the context."""
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


class VoterListView(VoterFilterMixin, ListView):
    """Display a paginated list of voters, with optional filtering."""

    model = Voter
    template_name = "voter_analytics/voter_list.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """Return the filtered queryset of voters."""
        return self.get_filtered_queryset()

    def get_context_data(self, **kwargs):
        """Add filter options and selected values to the template context."""
        context = super().get_context_data(**kwargs)
        return self.add_filter_context(context)


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


class GraphListView(VoterFilterMixin, ListView):
    """Display plotly graphs for filtered voter data."""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self):
        """Return the filtered queryset of voters."""
        return self.get_filtered_queryset()

    def get_context_data(self, **kwargs):
        """Add graphs and filter choices to the template context."""
        context = super().get_context_data(**kwargs)
        context = self.add_filter_context(context)

        qs = self.get_queryset()

        # Graph 1: distribution by year of birth
        birth_data = (
            qs.exclude(date_of_birth__isnull=True)
            .values("date_of_birth__year")
            .annotate(total=Count("id"))
            .order_by("date_of_birth__year")
        )

        birth_years = [item["date_of_birth__year"] for item in birth_data]
        birth_counts = [item["total"] for item in birth_data]

        birth_fig = go.Figure(
            data=[go.Bar(x=birth_years, y=birth_counts)]
        )
        birth_fig.update_layout(
            title="Distribution of Voters by Year of Birth",
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters",
        )
        context["birth_chart"] = plot(
            birth_fig, output_type="div", include_plotlyjs=False
        )

        # Graph 2: distribution by party affiliation
        party_data = (
            qs.values("party_affiliation")
            .annotate(total=Count("id"))
            .order_by("party_affiliation")
        )

        party_labels = [
            item["party_affiliation"].strip() if item["party_affiliation"].strip() else "(blank)"
            for item in party_data
        ]
        party_counts = [item["total"] for item in party_data]

        party_fig = go.Figure(
            data=[go.Pie(labels=party_labels, values=party_counts)]
        )
        party_fig.update_layout(
            title="Distribution of Voters by Party Affiliation"
        )
        context["party_chart"] = plot(
            party_fig, output_type="div", include_plotlyjs=False
        )

        # Graph 3: participation in elections
        election_fields = [
            ("v20state", "2020 State"),
            ("v21town", "2021 Town"),
            ("v21primary", "2021 Primary"),
            ("v22general", "2022 General"),
            ("v23town", "2023 Town"),
        ]

        election_labels = [label for field, label in election_fields]
        election_counts = [
            qs.filter(**{field: True}).count() for field, label in election_fields
        ]

        election_fig = go.Figure(
            data=[go.Bar(x=election_labels, y=election_counts)]
        )
        election_fig.update_layout(
            title="Voter Participation by Election",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
        )
        context["election_chart"] = plot(
            election_fig, output_type="div", include_plotlyjs=False
        )

        return context