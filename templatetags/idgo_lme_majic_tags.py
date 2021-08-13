from django import template
# from django.conf import settings

register = template.Library()

# settings value

@register.filter(is_safe=True)
def lookup(d, key=0):
    import pdb; pdb.set_trace()

    return d[key].jurisdiction.get_communes_as_feature_collection_geojson
    

# @register.filter(is_safe=True)
# def communes_list(d, key):
#     list_communes = list(d.values_list(key, flat=True))
#     str1_list_communes = ','.join(list_communes)
#     return str1_list_communes

