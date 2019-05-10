
from django.conf.urls import url
from django.contrib import admin
from .views import (
    LookupView)
    


urlpatterns = [
    url(r'^$', LookupView.as_view(), name='default'),
    

    
]

