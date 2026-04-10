from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    ProfileListView,
    ProfileDetailView,
    PostDetailView,
    CreatePostView,
    UpdateProfileView,
    UpdatePostView,
    DeletePostView,
    ShowFollowersDetailView,
    ShowFollowingDetailView,
    PostFeedListView,
    SearchView,
    MyProfileDetailView,
    CreateProfileView,
    FollowProfileView,
    DeleteFollowProfileView,
    LikePostView,
    DeleteLikePostView,
)


from .api_views import (
    api_root,
    CustomAuthToken,
    ProfileListAPIView,
    ProfileDetailAPIView,
    PostListCreateAPIView,
    PostDetailAPIView,
    ProfilePostsAPIView,
    ProfileFeedAPIView,
)

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),

    # API routes
    path("api/", api_root, name="api_root"),
    path("api/login", CustomAuthToken.as_view(), name="api_login"),
    path("api/profiles", ProfileListAPIView.as_view(), name="api_profiles"),
    path("api/profile/<int:pk>", ProfileDetailAPIView.as_view(), name="api_profile_detail"),
    path("api/profile/<int:pk>/posts", ProfilePostsAPIView.as_view(), name="api_profile_posts"),
    path("api/profile/<int:pk>/feed", ProfileFeedAPIView.as_view(), name="api_profile_feed"),
    path("api/posts", PostListCreateAPIView.as_view(), name="api_posts"),
    path("api/post/<int:pk>", PostDetailAPIView.as_view(), name="api_post_detail"),
    path("api/profile/<int:pk>/posts", ProfilePostsAPIView.as_view(), name="api_profile_posts"),
    path("api/profile/<int:pk>/feed", ProfileFeedAPIView.as_view(), name="api_profile_feed"),

    # Existing HTML routes
    path("profile", MyProfileDetailView.as_view(), name="show_my_profile"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),

    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),

    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/feed", PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", SearchView.as_view(), name="search"),

    path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(), name="show_following"),

    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="mini_insta/login.html",
            next_page=reverse_lazy("show_my_profile"),
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout",
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy("show_all_profiles")
        ),
        name="logout",
    ),

    path("create_profile", CreateProfileView.as_view(), name="create_profile"),

    path("profile/<int:pk>/follow", FollowProfileView.as_view(), name="follow_profile"),
    path("profile/<int:pk>/delete_follow", DeleteFollowProfileView.as_view(), name="delete_follow_profile"),
    path("post/<int:pk>/like", LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/delete_like", DeleteLikePostView.as_view(), name="delete_like_post"),
]