from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View
from recommendations.models import ActivityRecommendationView
from activities.models import Activity

def home(request):
    print(request)
    print(request.user)
    print(request.path)

    #return HttpResponse("Hello")
    return render(request, "home.html", {})

class HomeView(View):
    def get(self, request, *args, **kwargs): # GET -- To grab view / list view/ search
       activity_qs = Activity.objects.all().events().registered(request.user)
       qs = activity_qs.featured().distinct().order_by("?")[:5] # get random order of 5 items
       event_qs = ActivityRecommendationView.objects.all().prefetch_related("activity")
       if request.user.is_authenticated():
           event_views = event_qs.filter(user=request.user)
       else:
            event_views = event_qs.filter(views__gte=10)
       event_views = event_qs.order_by('views')[:30]
       ids_ = [i.activity.id for i in event_views]
       rec_activities = activity_qs.filter(id__in=ids_).order_by('?')[:5] # to control how many activity posts to be shown in the home page


       context = {
           "rec_activities": rec_activities,
           "qs": qs,
           "name": "Moe"
       }
       return render(request, "home.html", context)

   # def post(self, request, *args, **kwargs): # POST -- create View
       # return render("Hello")

    #def put(self, request, *args, **kwargs): # PUT -- Update View
        #return render("Hello")

    #def delete(self, request, *args, **kwargs): # DELETE -- delete view
        #return render("Hello")
