from django import template
# from django.conf import settings

register = template.Library()

# settings value

@register.filter(is_safe=True)
def lookup(d, key):
    import pdb; pdb.set_trace()
    return d[key]
