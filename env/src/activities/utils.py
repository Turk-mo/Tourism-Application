from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.text import slugify
import random
import string


def special_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def slug_generator(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.title)
    else:
        slug = new_slug
    Klass       = instance.__class__
    qs          = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        special_string        = special_string_generator()
        latest_generated_slug = slug + "-{id_}".format(id_=special_string) 
        return slug_generator(instance, new_slug=latest_generated_slug)
    return slug 

def generate_display_charge(charge):
     gbp = round(charge, 2)
     return "£%s%s" % (intcomma(int(gbp)), ("%0.2f" % gbp)[-3:])