from django.db import models
from django.db.models import Q
from django.shortcuts import render, reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from activities.utils import slug_generator
from django.core.validators import URLValidator




class PostQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


    def unused(self):
        return self.filter(Q(event__isnull=True)&Q(genre__isnull=True))

 

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()



class Post(models.Model):
    slug                        = models.SlugField(blank=True)
    title                       = models.CharField(max_length=90)
    city_info                   = models.TextField()
    # city             = models.
    social_media_link           = models.TextField(validators=[URLValidator()])
    embed_link                  = models.TextField(blank=True) #without blank=True means that it is a required field
    basic                       = models.BooleanField(default=True)
    member                      = models.BooleanField(default=False)
    timestamp                   = models.DateTimeField(auto_now_add=True) # what time it was added
    latest_update               = models.DateTimeField(auto_now=True) # what time it was saved
    
    objects          = PostManager()
                
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

def pre_save_post_reciever(sender, instance, *args, **kwargs):
    
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(pre_save_post_reciever, sender=Post)



"""
def post_save_post_reciever(sender, instance, created, *args, **kwargs):
    
    if not instance.slug:
        instance.slug = slugify(instance.title) #post_save does not auto save so instance.save() must be written
        instance.save()

post_save.connect(post_save_post_reciever, sender=Post)
"""