from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db.models import Prefetch, Q
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from .utils import slug_generator, generate_display_charge 
from posts.models import Post
from categories.models import Genre
from .fields import PositionField

   
class UserActivities(models.Model):
    user                = models.OneToOneField(settings.AUTH_USER_MODEL)
    activities          = models.ManyToManyField('Activity', related_name='registered', blank=True)
    timestamp           = models.DateTimeField(auto_now_add=True) # what time it was added
    latest_update       = models.DateTimeField(auto_now=True)

    def __str__(self):
         return str(self.activities.all().count())

    class Meta:
        verbose_name = 'My Activities'
        verbose_name_plural = 'My Activities'

def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        UserActivities.objects.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)

class ActivityQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    

    def events(self):
        return self.prefetch_related('event_set')

    def featured(self): # use this for the promoted activities on homepage
        return self.filter(Q(genre__slug__icontains='featured')) #| Q(secondary__slug='featured'))

    def registered(self, user):
        if user.is_authenticated():
            qs = UserActivities.objects.filter(user=user)
        else:
            qs = UserActivities.objects.none()
        return self.prefetch_related(
                Prefetch('registered',
                    queryset=qs,
                    to_attr='is_author'
                )
            )

class ActivityManager(models.Manager):
    def get_queryset(self):
        return ActivityQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()





def handle_image_upload(instance, filename):
    if instance.slug:
        return "%s/images/%s" %(instance.slug, filename)
    return "uknown/images/%s" %(filename)


class Activity(models.Model):
    user                = models.ForeignKey(settings.AUTH_USER_MODEL)
    title               = models.CharField(max_length=90)
    image_thumbanil     = models.ImageField(upload_to='activities', height_field='image_height', width_field='image_width', blank=True, null=True)
    image_height        = models.IntegerField(blank=True, null=True)
    image_width         = models.IntegerField(blank=True, null=True)
    post_order          = PositionField(collection='genre')
    city                = models.CharField(max_length=40)
    genre               = models.ForeignKey(Genre, related_name='primary_genre', null=True, blank=True)
    secondary            = models.ManyToManyField(Genre, related_name='secondary_genre', blank=True)
    #category_example    = models.CharField(max_length=110, choices=POSITION_CHOICES, default='main_choice')
    overview            = models.TextField() #without blank=True means that it is a required field
    charge              = models.DecimalField(decimal_places=2, max_digits=100)
    timestamp           = models.DateTimeField(auto_now_add=True) # what time it was added
    latest_update       = models.DateTimeField(auto_now=True)
    active              = models.BooleanField(default=True)
    slug                = models.SlugField(blank=True) # You can add #unique=True for extra validation
    post                = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    example             = models.CharField(max_length=45)
    objects = ActivityManager()

    
    def __str__(self):
        return self.title

    class Meta: # Verbose_name to change the name of the instances in the Admin page
        verbose_name = 'Activities'
        verbose_name_plural = 'Activities'

    def get_absolute_url(self):
        return reverse("activities:detail", kwargs={"slug": self.slug})

    def get_obtain_url(self):
        return reverse("activities:obtain", kwargs={"slug": self.slug})

    def display_charge_per_event(self):
        return generate_display_charge(self.charge)

def post_save_activity_reciever(sender, instance, created, *args, **kwargs):
    if not instsance.genre in instance.secondary.all():
        instance.secondary.add(instance.genre)
post_save.connect(post_save_activity_reciever, sender=Genre)

class Event(models.Model):
    activity            = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    title               = models.CharField(max_length=90)
    overview            = models.TextField() #without blank=True means that it is a required field
    post                = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    basic               = models.BooleanField(default=False)
    post_order          = PositionField(collection='activity')
    timestamp           = models.DateTimeField(auto_now_add=True) # what time it was added
    latest_update       = models.DateTimeField(auto_now=True)
    slug                = models.SlugField(blank=True) # You can add #unique=True for extra validation
    #charge              = models.DecimalField(decimal_places=3, max_digits=100) refer to video #35 @ 1:20

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('slug', 'activity'),)
        ordering        = ['post_order', 'title'] #'-order' is from 1-10, 'title' is from a-z

    
    def get_absolute_url(self):
        return reverse("activities:event-detail", 
        kwargs={
            "aslug": self.activity.slug,
            "eslug": self.slug
            }
            )


def pre_save_post_reciever(sender, instance, *args, **kwargs):
    
    if not instance.slug:
        instance.slug = slug_generator(instance)

pre_save.connect(pre_save_post_reciever, sender=Activity)
#pre_save.connect(pre_save_post_reciever, sender=Event)