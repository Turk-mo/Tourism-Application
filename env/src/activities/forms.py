from django.db.models import Q
from django import forms
from .models import Activity, Event, UserActivities
from posts.models import Post

class UserActivitiesForm(forms.ModelForm):
    class Meta:
        model = UserActivities
        fields = [
            'user',
            'activities',
        ]
        
class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            
            'title',
            'post',
            'basic',
            'overview',
            'post_order',
            'slug',
        ]
    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
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



class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title',
            'overview',
            'charge',
            'genre',
            'post',
            'image_thumbanil',
            # 'slug',
        ]

    def clean_slug(self): #clean_"field" to process form validation
        slug = self.cleaned_data.get("slug")
        qs = Activity.objects.filter(slug=slug)
        if qs.count() >= 1:
            raise forms.ValidationError("This Slug is taken, it must be unique")
        return slug

    def clean_charge(self): # You can use this same validation for any field above
        charge = self.cleaned_data.get("charge")
        qs = Activity.objects.filter(charge=charge)
        if qs.exists():
            raise forms.ValidationError("Charged price must be more than 5$")
        return charge