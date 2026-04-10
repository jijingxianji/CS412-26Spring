from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Profile, Post
from .serializers import ProfileSerializer, PostSerializer

from django.shortcuts import get_object_or_404


@api_view(["GET"])
def api_root(request):
    return Response({
        "POST /mini_insta/api/login": "log in and get token + profile_id",
        "GET /mini_insta/api/profiles": "list all profiles",
        "GET /mini_insta/api/profile/<pk>": "get one profile",
        "GET /mini_insta/api/profile/<pk>/posts": "get all posts for one profile",
        "GET /mini_insta/api/profile/<pk>/feed": "get feed for one profile",
        "GET /mini_insta/api/posts": "list all posts",
        "POST /mini_insta/api/posts": "create one post",
        "GET /mini_insta/api/post/<pk>": "get one post",
    })


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        profile = get_object_or_404(Profile, user=user)

        return Response({
            "token": token.key,
            "profile_id": profile.pk,
            "username": user.username,
        })


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all().order_by("username")
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-timestamp")
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        my_profile = get_object_or_404(Profile, user=self.request.user)
        posted_profile = serializer.validated_data.get("profile")

        if posted_profile and posted_profile != my_profile:
            raise PermissionDenied("You can only create posts for your own profile.")

        serializer.save(profile=my_profile)


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ProfilePostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return profile.get_all_posts()


class ProfileFeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return profile.get_post_feed()