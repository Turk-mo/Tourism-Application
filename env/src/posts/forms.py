from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ # These fields are grabbed from Post models, you can add any updated ones
            'title',
            'embed_link',
            'social_media_link',
            'member'
        ]