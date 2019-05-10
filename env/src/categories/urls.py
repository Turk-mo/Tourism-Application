
from django.conf.urls import url

from .views import (
    GenreListView, 
    GenreDetailView,
)

urlpatterns = [
    url(r'^$', GenreListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', GenreDetailView.as_view(), name='detail'),

    
]


   