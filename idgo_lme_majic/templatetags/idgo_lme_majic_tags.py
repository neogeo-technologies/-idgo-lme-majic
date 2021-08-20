from django import template
# from django.conf import settings

register = template.Library()

@register.filter(is_safe=True)
def lookup(d, key=0):
    return d[key]