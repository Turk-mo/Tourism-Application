from django import template
register = template.Library()

@register.inclusion_tag('lookup/snippets/lookup_form.html')
def lookup_form(request, navbar=False):
    return {"request": request, 'navbar': navbar}