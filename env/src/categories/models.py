from django.db import models
from django.db.models import Count
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from activities.utils import slug_generator
from activities.fields import PositionField
from posts.models import Post




class GenreQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

 

class GenreManager(models.Manager):
    def get_queryset(self):
        return GenreQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all(
            ).active().annotate(
                activities_length= Count("secondary_genre", distinct=True)
            ).prefetch_related('primary_genre', 'secondary_genre')


class Genre(models.Model):
    title               = models.CharField(max_length=80)
    post                = models.ForeignKey(Post, null=True, blank=True)
    order               = PositionField(blank=True)
    overview            = models.TextField()
    active              = models.BooleanField(default=True)
    timestamp           = models.DateTimeField(auto_now_add=True) 
    latest_update       = models.DateTimeField(auto_now=True)
    slug                = models.SlugField(blank=True)

    objects = GenreManager()

    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


def pre_save_genre_reciever(sender, instance, *args, **kwargs):    
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(pre_save_genre_reciever, sender=Genre)



