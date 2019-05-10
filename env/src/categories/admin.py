from django.contrib import admin

from .models import Genre
from .forms import GenreAdminForm







class GenreAdmin(admin.ModelAdmin):
    readonly_fields = ['short_title','latest_update', 'timestamp']
    list_display = ['title','latest_update', 'timestamp']
    list_filter = ['latest_update', 'timestamp']
    search_fields = ['title']
    form = GenreAdminForm
    
    #class Meta:
      #  model = Genre

    def short_title(self, object):
        return object.title[:10]

admin.site.register(Genre, GenreAdmin)
