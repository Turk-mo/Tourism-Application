from django import forms
from django.db.models import Q
from .models import Genre
from posts.models import Post






class GenreAdminForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = [
            'title',
            'post',
            'overview',
            'order',
            'slug',
        ]
    def __init__(self, *args, **kwargs):
        super(GenreAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get("instance")
        qs = Post.objects.all().unused()
        if obj:
            #qs = Post.objects.exclude(event__activity=obj.activity).exclude(event__isnull=False)
            if obj.post:
                this_ = Post.objects.filter(pk=obj.post.pk)
                qs = (qs | this_)
            self.fields['post'].queryset = qs
        else:
            #qs = Post.objects.filter(event__isnull=True)
            self.fields['post'].queryset = qs