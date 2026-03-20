"""
models.py
Yilin Lyu, jixian77@bu.edu

Model and data-loading helpers for the voter_analytics app.
"""

import csv
import datetime
from pathlib import Path

from django.conf import settings
from django.db import models


class Voter(models.Model):
    """Model representing one voter record from the Newton voter CSV file."""

    voter_id = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a readable string representation of this voter."""
        return f"{self.first_name} {self.last_name}"

    def street_address(self):
        """Return the formatted street address for this voter."""
        if self.apartment_number:
            return f"{self.street_number} {self.street_name}, Apt {self.apartment_number}"
        return f"{self.street_number} {self.street_name}"


def string_to_bool(value):
    """Convert a CSV TRUE/FALSE string into a Python boolean."""
    return value == "TRUE"


def parse_date(value):
    """Convert a date string from the CSV into a Python date."""
    value = value.strip()

    if not value:
        return None

    # try common formats first
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    # handle bad placeholder dates like 1900-01-00 or 01/00/1900
    if value.endswith("-00") or "/00/" in value:
        return None

    raise ValueError(f"Bad date value: {value}")



def load_data():
    """
    Load voter data from newton_voters.csv into the database.

    The CSV file should be stored in the project root directory,
    alongside manage.py.

    Returns:
        int: the number of records processed
    """
    filename = Path(settings.BASE_DIR) / "newton_voters.csv"

    if not filename.exists():
        raise FileNotFoundError(f"Could not find data file: {filename}")

    count = 0

    with open(filename, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            Voter.objects.update_or_create(
                voter_id=row["Voter ID Number"],
                defaults={
                    "last_name": row["Last Name"],
                    "first_name": row["First Name"],
                    "street_number": row["Residential Address - Street Number"],
                    "street_name": row["Residential Address - Street Name"],
                    "apartment_number": row["Residential Address - Apartment Number"],
                    "zip_code": row["Residential Address - Zip Code"].zfill(5),
                    "date_of_birth": parse_date(row["Date of Birth"]),
                    "date_of_registration": parse_date(row["Date of Registration"]),
                    "party_affiliation": row["Party Affiliation"].strip(),
                    "precinct_number": row["Precinct Number"].strip(),
                    "v20state": string_to_bool(row["v20state"]),
                    "v21town": string_to_bool(row["v21town"]),
                    "v21primary": string_to_bool(row["v21primary"]),
                    "v22general": string_to_bool(row["v22general"]),
                    "v23town": string_to_bool(row["v23town"]),
                    "voter_score": int(row["voter_score"]),
                },
            )
            count += 1

    return count