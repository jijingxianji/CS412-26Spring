#from django.shortcuts import render

# Create your views here.

# generic ListView : will automatically complete the routine work of "checking all records → passing to the template"
from django.views.generic import ListView, DetailView
from .models import Profile

class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"
    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"
