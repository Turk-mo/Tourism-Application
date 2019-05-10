from django.db import models
from django.conf import settings
from activities.models import Activity

class ActivityRecommendationView(models.Model):
    user                 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    activity            = models.ForeignKey(Activity)
    views              = models.IntegerField(default=0)
    latest_update       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.views)
