from django.contrib import admin

from .models import Post



class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['short_title','latest_update', 'timestamp']
    list_display = ['title','latest_update', 'timestamp']
    list_filter = ['latest_update', 'timestamp']
    search_fields = ['title']
    
    class Meta:
        model = Post

    def short_title(self, object):
        return object.title[:10]

admin.site.register(Post, PostAdmin)

