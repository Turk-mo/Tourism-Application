from django.contrib import admin
from .models import Activity, Event, UserActivities
from .forms import EventAdminForm


class EventInline(admin.TabularInline):
    model = Event
    form  = EventAdminForm 
    prepopulated_fields = {"slug": ("title",)}
    extra = 1
class ActivityAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    readonly_fields = ['short_title','latest_update', 'timestamp']
    list_filter = ['latest_update', 'timestamp']
    list_display = ['title','latest_update', 'timestamp', 'post_order']
    search_fields = ['title', 'overview']
    list_editable = ['post_order']
    
    class Meta:
        model = Activity

    def short_title(self, object):
        return object.title[:10]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(UserActivities)