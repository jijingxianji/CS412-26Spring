#from django.shortcuts import render

# Create your views here.

# generic ListView : will automatically complete the routine work of "checking all records → passing to the template"
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm


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
        form.instance.profile = profile  # 解决 NOT NULL profile_id

        response = super().form_valid(form)  # 先保存 Post，self.object 就是新 Post

        image_url = self.request.POST.get("image_url")
        if image_url:
            Photo.objects.create(post=self.object, image_url=image_url)

        return response