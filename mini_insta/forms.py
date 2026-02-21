
from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]   # 不要放 profile；profile 来自 URL 的 pk
