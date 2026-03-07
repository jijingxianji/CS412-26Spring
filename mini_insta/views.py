#from django.shortcuts import render

# Create your views here.

# generic ListView : will automatically complete the routine work of "checking all records → passing to the template"
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
# A6
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import date


# A6: new mixins for login required and owner only access control
class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse("login")

    def get_user_profile(self):
        return Profile.objects.get(user=self.request.user)

class OwnerOnlyPostMixin(MiniInstaLoginRequiredMixin):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.profile.user != self.request.user:
            raise PermissionDenied
        return obj

class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            context["my_profile"] = my_profile
            context["is_following"] = my_profile.is_following(self.object)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            context["my_profile"] = my_profile
            context["is_liked"] = self.object.is_liked_by(my_profile)
        return context
    

# A6: new mixin for login required access control, and refactor CreatePostView to use the mixin
class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_user_profile()
        return context

    def form_valid(self, form):
        form.instance.profile = self.get_user_profile()

        response = super().form_valid(form)

        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response
    
# A6: new view for updating profile, which requires login and owner-only access control
class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self, queryset=None):
        return self.get_user_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object
        return context
    

class UpdatePostView(OwnerOnlyPostMixin, UpdateView): 
    # only allow updating post if the current user is the owner of the post
    model = Post
    fields = ["caption"]  # only allow updating caption, not profile
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile  # for base.html to show the profile's username in the title
        return context


class DeletePostView(OwnerOnlyPostMixin, DeleteView): 
    # only allow deleting post if the current user is the owner of the post
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
    
# A5: new views for showing followers and following lists
class ShowFollowersDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_followers.html"

class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"

# A5: new view for showing post feed
class PostFeedListView(MiniInstaLoginRequiredMixin, ListView): 
    # only allow showing post feed if the user is logged in
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.profile = self.get_user_profile()
        return self.profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context
    
# A5: new view for search results
class SearchView(MiniInstaLoginRequiredMixin, ListView): 
    # only allow showing search results if the user is logged in
    model = Post
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_user_profile()
        self.q = request.GET.get("q", "").strip()

        if not self.q:
            return render(request, "mini_insta/search.html", {"profile": self.profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(caption__icontains=self.q).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        context["q"] = self.q
        context["profiles"] = (
            Profile.objects.filter(username__icontains=self.q)
            | Profile.objects.filter(display_name__icontains=self.q)
        )
        return context
    

# A6: new views for showing own profile and updating own profile, which require login and owner-only access control
class MyProfileDetailView(MiniInstaLoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.get_user_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_profile"] = self.object
        context["is_following"] = False
        return context
    

# A6: new view for creating profile, which also creates a new user account and logs in the user after successful creation
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

        new_user = user_form.save()
        login(self.request, new_user)

        form.instance.user = new_user
        form.instance.join_date = date.today()

        return super().form_valid(form)
    

class FollowProfileView(MiniInstaLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        my_profile = self.get_user_profile()

        if target_profile == my_profile:
            raise PermissionDenied

        Follow.objects.get_or_create(
            profile=target_profile,
            follower_profile=my_profile,
        )
        return redirect("show_profile", pk=target_profile.pk)


class DeleteFollowProfileView(MiniInstaLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        my_profile = self.get_user_profile()

        Follow.objects.filter(
            profile=target_profile,
            follower_profile=my_profile,
        ).delete()

        return redirect("show_profile", pk=target_profile.pk)

# A6: new views for liking and unliking post, which require login but not owner-only access control (users can like/unlike any post, just not their own posts)
class LikePostView(MiniInstaLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_obj = get_object_or_404(Post, pk=self.kwargs["pk"])
        my_profile = self.get_user_profile()

        if post_obj.profile == my_profile:
            raise PermissionDenied

        Like.objects.get_or_create(
            post=post_obj,
            profile=my_profile,
        )
        return redirect("show_post", pk=post_obj.pk)

# A6: new view for unliking post
class DeleteLikePostView(MiniInstaLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_obj = get_object_or_404(Post, pk=self.kwargs["pk"])
        my_profile = self.get_user_profile()

        Like.objects.filter(
            post=post_obj,
            profile=my_profile,
        ).delete()

        return redirect("show_post", pk=post_obj.pk)