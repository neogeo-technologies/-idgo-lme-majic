import operator


from django import template
from django.shortcuts import render

from idgo_lme_majic.forms import MajicForm
from idgo_lme_majic.models import UserMajicLme
from idgo_lme_majic.views.common import DECORATORS
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from idgo_admin.models import Organisation
from idgo_admin.models import BaseMaps
from idgo_admin.models import Profile


register = template.Library()

@register.filter
def get_by_index(l, i):
    return l[i]


# Create your views here.


# def handler_get_request(request):
#     user = request.user
#     if user.profile.is_admin:
#         datasets = Dataset.objects.all()
#     else:
#         s1 = set(Dataset.objects.filter(organisation__in=user.profile.referent_for))
#         s2 = set(Dataset.objects.filter(editor=user))
#         datasets = list(s1 | s2)
#     return datasets

@method_decorator(DECORATORS, name='dispatch')
class MajicCreate(CreateView):

    # model = UserMajicLme

    form_class = MajicForm

    template_name = 'idgo_lme_majic/majic/majic.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        organisations = []
        
        try:
            majics = UserMajicLme.objects.filter(user=request.user)
        except UserMajicLme.DoesNotExist:
            majics = None
        # import pdb; pdb.set_trace()
        # for instance in Profile.objects.get(user=request.user).referents.all().exclude(id__in=majics):
        idx = 0
        for instance in Profile.objects.get(user=request.user).referents.all():
            
            organisations.append({
                'organisation_pk': idx,
                'pk': instance.pk,
                'legal_name': instance.legal_name,
                'jurisdiction': instance.jurisdiction,
                'member': (instance == profile.organisation),
                'contributor': (instance in profile.contribute_for),
                'referent': profile.is_admin and True or (instance in profile.referent_for),
                })
            idx+=1
        
        context = {
            'profile': profile,
            'majics' : majics,
            'form': self.form_class,
            'basemaps': BaseMaps.objects.all(),
            'organisations': organisations,
            }
        # import pdb; pdb.set_trace()
        return render(request, self.template_name, context=context)
    
    @register.filter
    def return_item(l, i):
        try:
            return l[i]
        except:
            return None

    # @register.filter
    # def index(indexable, i):
    #     return indexable[i]
