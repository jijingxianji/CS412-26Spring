#from django.shortcuts import render

# Create your views here.

# generic ListView : will automatically complete the routine work of "checking all records → passing to the template"
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse
from django.shortcuts import render


class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        context["profile"] = profile
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        form.instance.profile = profile

        response = super().form_valid(form)  # saves Post first

        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response
    

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object  # let base.html know which profile is being updated
        return context
    

class UpdatePostView(UpdateView):
    model = Post
    fields = ["caption"]  # only allow updating caption, not profile
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile  # for base.html to show the profile's username in the title
        return context


class DeletePostView(DeleteView):
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
class PostFeedListView(ListView):
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.profile = Profile.objects.get(pk=self.kwargs["pk"])
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context
    
# A5: new view for search results
class SearchView(ListView):
    model = Post
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        self.profile = Profile.objects.get(pk=self.kwargs["pk"])
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
        context["profiles"] = Profile.objects.filter(
            username__icontains=self.q
        ) | Profile.objects.filter(
            display_name__icontains=self.q
        )
        return context