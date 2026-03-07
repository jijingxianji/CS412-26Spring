# mini_insta/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    username = models.CharField(max_length=60, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(max_length=500)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.username}({self.display_name})"

    def get_absolute_url(self):
        return reverse("show_profile", kwargs={"pk": self.pk})

    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by("-timestamp")
    
    def get_followers(self):
        return [f.follower_profile for f in self.followers.all()]

    def get_num_followers(self):
        return self.followers.count()

    def get_following(self):
        return [f.profile for f in self.following.all()]

    def get_num_following(self):
        return self.following.count()
    
    def get_post_feed(self):
        following_profiles = self.get_following()   # list of Profile
        return Post.objects.filter(profile__in=following_profiles).order_by("-timestamp")
    
    def is_following(self, other_profile):
        return Follow.objects.filter(
            follower_profile=self,
            profile=other_profile
        ).exists()


class Post(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post {self.pk} by {self.profile.username}"

    def get_absolute_url(self):
        return reverse("show_post", kwargs={"pk": self.pk})

    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by("timestamp")

    def get_first_photo(self):
        return self.get_all_photos().first()
    
    def get_all_comments(self):
        return Comment.objects.filter(post=self).order_by("timestamp")

    def get_likes(self):
        return Like.objects.filter(post=self)
    
    def is_liked_by(self, profile):
        return Like.objects.filter(post=self, profile=profile).exists()


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # A5: keep image_url for backward compatibility, but make it optional
    image_url = models.URLField(max_length=500, blank=True)

    # A5: new uploaded file field
    image_file = models.ImageField(upload_to="mini_insta", blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.pk} for Post {self.post.pk}"

    def get_image_url(self):
        """
        Prefer the old image_url if present; otherwise use uploaded file url.
        """
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""
    
    # It allows you to use the {% url %} template tag with Photo objects.
    def get_absolute_url(self):
        return reverse("show_photo", kwargs={"pk": self.pk})
    
class Follow(models.Model):
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="followers"   # who follows me (Follow objects)
    )
    follower_profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="following"   # who I follow (Follow objects)
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_profile.username} follows {self.profile.username}"
    
# A5: new models for comments and likes
class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.pk} on Post {self.post.pk}"

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="likes",
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.profile:
            return f"{self.profile.username} likes Post {self.post.pk}"
        return f"Like {self.pk} on Post {self.post.pk}"
