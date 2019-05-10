from django.shortcuts import render
from .models import Genre
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    RedirectView,
    DeleteView
)


class GenreListView(ListView):
    queryset = Genre.objects.all().order_by('title') #You can add other fields here too


class GenreDetailView(DetailView):
    queryset = Genre.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(GenreDetailView, self).get_context_data(*args, **kwargs)
        obj = context.get("object")
        user = self.request.user
        qsone = obj.primary_genre.all().registered(self.request.user)
        context['featured_activities'] = qsone[:4] # number of featured courses handled here
        qstwo = obj.secondary_genre.all().registered(self.request.user)
        qs = (qsone | qstwo).distinct()
        context ['activities'] = qs 
        return context
