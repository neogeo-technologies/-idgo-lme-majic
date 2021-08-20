import io
import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import FileResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from idgo_admin.models import Organisation
from idgo_admin.models import BaseMaps
from idgo_admin.models import Profile

from idgo_lme_majic.forms import MajicForm
from idgo_lme_majic.models import UserMajicLme
from idgo_lme_majic.export_api import check_majic_export_api
from idgo_lme_majic.export_api import check_url
from idgo_lme_majic.export_api import download_file
from idgo_lme_majic.utils import add_years
from idgo_lme_majic.utils import send_demande_extraction_majic_lme
from idgo_lme_majic.views.common import DECORATORS


@method_decorator(DECORATORS, name='dispatch')
class MajicCreate(CreateView):

    form_class = MajicForm

    template_name = 'idgo_lme_majic/majic/majic.html'

    statut_and_url = {}

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
            }

        return context
    
    def post(self, request):
        user = request.user
        if 'majic' in request.POST:
            form = MajicForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.date_expiration_majic = add_years(datetime.today(), 1)
                instance.save()
                file_declaration = request.FILES['fileDeclaration']
                file_clause = request.FILES['fileClause']
                files = [
                    file_declaration,
                    file_clause,
                ]
                url = instance.get_full_admin_url()
                send_demande_extraction_majic_lme(instance.user, 'MAJIC', instance.organisation, url, files)

        return redirect('idgo_lme_majic:majic')


# @method_decorator(DECORATORS, name='dispatch')
@login_required()
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
                if mode == '{}':
                    mode = ''
                statut_and_url = check_majic_export_api(str_list_communes,secret, request_id, mode)
    
    return JsonResponse(statut_and_url)


# @method_decorator(DECORATORS, name='dispatch')
@login_required()
def download_majic(request):
    response = {}
    if request.method == 'GET':
        if 'request_id' in request.GET:
            request_id = request.GET['request_id']
            type_ext = request.GET['type']
            res = download_file(request_id, type_ext)
            if res.status_code == 200:
                file_zip = io.BytesIO(res.content)
                content_type = res.headers['Content-type']
                response = FileResponse(file_zip,  content_type=content_type)
            else:
                return JsonResponse({'success':False, 'errorMsg':'file error'})
    return response


# @method_decorator(DECORATORS, name='dispatch')
@login_required()
def geojson(request):
    
    geojson = {}
    if request.method == 'GET':
        if 'organisation' in request.GET:
            organisation = request.GET['organisation']
            try:
                obj_organisation = Organisation.objects.get(pk=organisation)
            except Organisation.DoesNotExist as e:
                obj_organisation = []
            geojson = json.loads(obj_organisation.jurisdiction.get_communes_as_feature_collection_geojson())
    return JsonResponse(geojson)