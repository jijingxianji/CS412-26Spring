

from django.db import models

from django.urls import reverse

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
     
     def get_all_posts(self):
          """Return all posts for this profile, newest first."""
          return Post.objects.filter(profile=self).order_by('-timestamp')


class Post(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post {self.pk} by {self.profile.username}"

    def get_absolute_url(self):
        return reverse("show_post", kwargs={"pk": self.pk})

    def get_all_photos(self):
        """Return all photos for this post."""
        return Photo.objects.filter(post=self).order_by("timestamp")

    def get_first_photo(self):
        return self.get_all_photos().first()
    

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.pk} for Post {self.post.pk}"