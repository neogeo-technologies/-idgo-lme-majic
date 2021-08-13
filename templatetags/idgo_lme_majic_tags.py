from django import template
# from django.conf import settings

register = template.Library()

# settings value

@register.filter(is_safe=True)
def lookup(d, key):
    return d[key]

@register.filter(is_safe=True)
def communes_list(d, key):
    list_communes = list(d.values_list(key, flat=True))
    str1_list_communes = ','.join(list_communes)
    return str1_list_communes

