from rest_framework import serializers
from .models import Profile, Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "image", "timestamp"]

    def get_image(self, obj):
        url = obj.get_image_url()
        request = self.context.get("request")

        if request and url:
            return request.build_absolute_uri(url)
        return url


class ProfileSerializer(serializers.ModelSerializer):
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "display_name",
            "profile_image_url",
            "bio_text",
            "join_date",
            "num_followers",
            "num_following",
        ]

    def get_num_followers(self, obj):
        return obj.get_num_followers()

    def get_num_following(self, obj):
        return obj.get_num_following()


class PostSerializer(serializers.ModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(),
        source="profile",
        write_only=True,
    )
    profile_username = serializers.CharField(
        source="profile.username",
        read_only=True,
    )
    photos = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "profile_id",
            "profile_username",
            "caption",
            "timestamp",
            "photos",
            "num_likes",
        ]

    def get_photos(self, obj):
        photos = obj.get_all_photos()
        return PhotoSerializer(photos, many=True, context=self.context).data

    def get_num_likes(self, obj):
        return obj.get_likes().count()