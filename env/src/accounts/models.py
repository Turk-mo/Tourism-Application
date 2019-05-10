from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from activities.models import Activity


# def handle_image_upload(instance, filename):
#     if instance.slug:
#         return "%s/images/%s" %(instance.slug, filename)
#     return "uknown/images/%s" %(filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, primary_key=True, related_name="user")
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', blank=True)
    bio   = models.CharField(max_length=145, default='')
    city  = models.CharField(max_length=145, default='')
    activity = models.ForeignKey(Activity)
    # picture                 = models.ImageField(default='default.jpg')
    
    # image_height            = models.IntegerField(blank=True, null=True)
    # image_width             = models.IntegerField(blank=True, null=True)
    # slug                     = models.SlugField(blank=True)

    def __str__(self):
        return f'{self.user.username} UserProfile'


    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)