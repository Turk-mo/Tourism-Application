
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from accounts import views as accounts_views

from .views import HomeView, home

urlpatterns = [
    url(r'^$', HomeView.as_view() , name='home'),
    url(r'^register/', accounts_views.register , name='register'),
    url(r'^profile/', accounts_views.profile , name='profile'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='accounts/login.html') , name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html') , name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^categories/', include('categories.urls', namespace='categories')),# Redirections to categories URLS
    url(r'^activities/', include('activities.urls', namespace='activities')),# Redirections to activities URLS
    url(r'^lookup/', include('lookup.urls', namespace='lookup')),# Redirections to lookup URLS
    url(r'^posts/', include('posts.urls', namespace='posts')),# Redirections to posts URLS
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

