from django.shortcuts import render
from django.views.generic import View 
from django.db.models import Q

#import the models you would like to apply lookup to
from activities.models import Activity, Event
from categories.models import Genre


class LookupView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        qs = None #general lookup
        g_qs = None #Genre lookup
        e_qs = None #Event lookup
        if query:
            event_search = Q(title__icontains=query) | Q(overview__icontains=query)
            query_search = event_search | Q(title__icontains=query) | Q(genre__title__icontains=query) | Q(event__title__icontains=query)
            
            qs = Activity.objects.all().events().filter(query_search).distinct()
            qs_ids = [i.id for i in qs]

            gen_search = Q(primary_genre__in=qs_ids) | Q(secondary_genre__in=qs_ids)
            g_qs = Genre.objects.filter(event_search | gen_search).distinct()
            e_qs = Event.objects.filter(event_search).distinct()

        context = {"qs": qs, "g_qs":g_qs, "e_qs":e_qs}
        return render(request, "lookup/default.html", context)
