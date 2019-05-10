
from django.conf.urls import url

from .views import (
    ActivityListView, 
    ActivityDetailView,
    ActivityCreateView,
    ActivityDeleteView,
    ActivityUpdateView,
    ActivityObtainView,
    EventDetailView
)

urlpatterns = [
    url(r'^$', ActivityListView.as_view(), name='list'),
    url(r'^create/$', ActivityCreateView.as_view(), name='create'),
    #url(r'^(?P<aslug>[\w-]+)/$', ActivityDetailView.as_view(), name='detail'), # changed from detail-slug to detail
    url(r'^(?P<slug>[\w-]+)/$', ActivityDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/obtain/$', ActivityObtainView.as_view(), name='obtain'),
    url(r'^(?P<aslug>[\w-]+)/(?P<eslug>[\w-]+)$', EventDetailView.as_view(), name='event-detail'),    
    url(r'^(?P<slug>[\w-]+)/update/$', ActivityUpdateView.as_view(), name='update'),
    url(r'(?P<slug>[\w-]+)/delete/$', ActivityDeleteView.as_view(), name='delete'),

    
]


   