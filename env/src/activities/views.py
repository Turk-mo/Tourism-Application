import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from posts.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from django.http import Http404
from django.db.models import Prefetch
from .models import Activity, Event, UserActivities
from .forms import ActivityForm
#from .forms import PostForm
from recommendations.models import ActivityRecommendationView
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    RedirectView,
    DeleteView,
    View
)
# can change this based on which one I decide to go with, staff if for specific group, member for everyone
class ActivityCreateView(StaffMemberRequiredMixin, CreateView): #check if StaffMemberRequriedMixin is the right one
    model = Activity
    form_class = ActivityForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(ActivityCreateView, self).form_valid(form)

class EventDetailView(View):
    def get(self, request, aslug=None, eslug=None, *args, **kwargs):
        obj = None
        qs = Activity.objects.filter(slug=aslug).events().registered(self.request.user) #slug=aslug will fetch for activitiy objects from db
        if not qs.exists():
            raise Http404
        activity_ = qs.first()
        if self.request.user.is_authenticated():
            #activity_ = None
            view_event, created = ActivityRecommendationView.objects.get_or_create(user=request.user, activity=activity_)
            if view_event:
                view_event.views += 1
                view_event.save()
        
        activity_ = qs.first()
        events_qs = activity_.event_set.filter(slug=eslug) # filters db for events
        if not events_qs.exists():
            raise Http404
        
        obj = events_qs.first()
        
        context = {
            "object": obj,
            "activity": activity_,

        }


        if not activity_.is_author and not obj.basic:
            return render(request, "activities/must_be_premium.html", {"object": activity_})

        return render(request, "activities/event_detail.html", context)
    """    
    def get_object(self):
        activity_slug = self.kwargs.get("aslug")
        event_slug    = self.kwargs.get('eslug')
        obj           = get_object_or_404(Event, activity__slug=activity_slug, slug=event_slug)
        return obj
    """
class ActivityDetailView(DetailView):
    #queryset = Activity.objects.all()
    def get_object(self):
        slug = self.kwargs.get("slug")
        qs = Activity.objects.filter(slug=slug).events().registered(self.request.user) #slug=aslug will fetch for activitiy objects from db
        #qs = Activity.objects.filter(slug=slug).registered(self.request.user) # returns a list of objects
        if qs.exists():
            obj = qs.first()
            if self.request.user.is_authenticated():
                view_event, created = ActivityRecommendationView.objects.get_or_create(user=self.request.user, activity=obj)
                if view_event:
                    view_event.views += 1
                    view_event.save()
            return obj
        raise Http404



class ActivityObtainView(LoginRequiredMixin, RedirectView):
    permanent = False
    #query_string = True
    def get_redirect_url(self, slug=None):
        qs = Activity.objects.filter(slug=slug).registered(self.request.user) # returns a list of objects
        if qs.exists():
            user = self.request.user
            if user.is_authenticated():
                user_activities = user.useractivities
                # run transaction
                # if the transaction is successful:
                user_activities.activities.add(qs.first())
                return qs.first().get_absolute_url()
            return qs.first().get_absolute_url()
        return "/activities/"


    

class ActivityListView(ListView):
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(ActivityListView, self).get_context_data(*args, **kwargs)
        print(context)
        return context
    
    def get_queryset(self):   
        request = self.request
        qs = Activity.objects.all()
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(title__icontains=query)
        if user.is_authenticated():
            qs =qs.registered(user)
        return qs


class ActivityUpdateView(StaffMemberRequiredMixin, UpdateView):
    queryset = Activity.objects.all()
    form_class = ActivityForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if not self.request.user.is_staff:
            obj.user = self.request.user
        obj.save()
        return super(ActivityUpdateView, self).form_valid(form)

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Activity.objects.filter(slug=slug) # returns a list of objects
        if obj.exists():
            return obj.first() # returns first instance of a list
        raise Http404

class ActivityDeleteView(StaffMemberRequiredMixin, DeleteView):
    queryset = Activity.objects.all()
    success_url = '/activities/'

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Activity.objects.filter(slug=slug) # returns a list of objects
        if obj.exists():
            return obj.first() # returns first instance of a list
        raise Http404
