

from django.db import models

# Create your models here.

class Profile(models.Model):
     username = models.CharField(max_length=60, unique=True)
     display_name = models.CharField(max_length=100)
     profile_image_url = models.URLField(max_length=500)
     bio_text = models.TextField(blank=True)
     join_date = models.DateField()

     def __str__(self) -> str:
          # is the most important readable representation during (admin) debugging
          return f"{self.username}({self.display_name})"
