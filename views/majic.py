import io

from django.conf import settings

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import FileResponse
from datetime import datetime
from datetime import date

from idgo_admin.models import Organisation
from idgo_admin.models import BaseMaps
from idgo_admin.models import Profile

from idgo_lme_majic.forms import MajicForm
from idgo_lme_majic.models import UserMajicLme
from idgo_lme_majic.views.common import DECORATORS
from idgo_lme_majic.export_api import check_majic_export_api
from idgo_lme_majic.export_api import check_url
from idgo_lme_majic.export_api import download_file
from idgo_lme_majic.utils import add_years

@method_decorator(DECORATORS, name='dispatch')
class MajicCreate(CreateView):
    # model = UserMajicLme
    form_class = MajicForm

    template_name = 'idgo_lme_majic/majic/majic.html'
    statut_and_url = {}

    # def get(self, request, *args, **kwargs):
    def get_context_data(self, *args, **kwargs):
        profile = self.request.user.profile
        organisations = []
        today = datetime.today()
        try:
            majics = UserMajicLme.objects.filter(user=self.request.user
                ).filter(date_expiration_majic__gte=today).distinct('organisation')
        except UserMajicLme.DoesNotExist:
            majics = None
        idx = 0
        for instance in Profile.objects.get(user=self.request.user
            ).referents.exclude(organisation__in=majics):
            
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
            'statut_and_url': self.statut_and_url,
            }

        # return render(self.request, self.template_name, context=context)
        return context
    
    def post(self, request):
        user = request.user
        if 'majic' in request.POST:
            form = MajicForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.date_expiration_majic = add_years(datetime.today(), 1)
                instance.majic = True
                instance.save()
                
                # TODO: ENVOYER MAIL AUX ADMINS AVEC LES FICHIER in REQUEST.FILES 
                #Mail.depot_demande()

        return redirect('idgo_lme_majic:majic')


# @method_decorator(DECORATORS, name='dispatch')
def majic_check(request):
    
    statut_and_url = {
        'statut': 'error',
        'url':'',
    }
    if request.method == 'GET':
        if 'statut' in request.GET:
            if request.GET['statut'] == 'pending':
                url = request.GET['url']
                request_id = request.GET['request_id']
                statut_and_url = check_url(url, request_id)
            elif 'request_id' in request.GET:
                request_id = request.GET['request_id']
                organisation = Organisation.objects.get(pk=request.GET['organisation'])
                list_communes = list(organisation.jurisdiction.communes.values_list('code', flat=True))
                str_list_communes = ','.join(list_communes)
                secret = request.GET['secret']
                mode = request.GET['mode']
                statut_and_url = check_majic_export_api(str_list_communes,secret, request_id, mode)
    
    return JsonResponse(statut_and_url)

def download_majic(request):
    res = {}
    if request.method == 'GET':
        if 'request_id' in request.GET:
            request_id = request.GET['request_id']
            res = download_file(request_id)
            import pdb; pdb.set_trace()
            file_zip = io.BytesIO(res.content)
            content_type = res.headers['Content-type']
            response = FileResponse(file_zip,  content_type=content_type)
    return response