from datetime import datetime
import mimetypes

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from idgo_admin.models import Organisation
from idgo_admin.models import BaseMaps
from idgo_admin.models import Profile
from idgo_admin.models.mail import send_demande_extraction_majic_lme

from idgo_lme_majic.models import UserMajicLme
from idgo_lme_majic.forms import MajicForm
from idgo_lme_majic.views.common import DECORATORS
from idgo_lme_majic.export_api import check_majic_export_api
from idgo_lme_majic.export_api import check_url
from idgo_lme_majic.utils import add_years


@method_decorator(DECORATORS, name='dispatch')
class LmeCreate(CreateView):

    model = UserMajicLme

    form_class = MajicForm

    template_name = 'idgo_lme_majic/lme/lme.html'

    def get_context_data(self, *args, **kwargs):
        profile = self.request.user.profile
        organisations = []
        today = datetime.today()
        try:
            lmes = UserMajicLme.objects.filter(user=self.request.user
                ).filter(date_expiration_lme__gte=today).distinct('organisation')
        except UserMajicLme.DoesNotExist:
            lmes = None
        
        idx = 0
        for instance in Profile.objects.get(user=self.request.user
            ).referents.exclude(organisation__in=lmes):
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
            'lmes' : lmes,
            'form': self.form_class,
            'basemaps': BaseMaps.objects.all(),
            'organisations': organisations,
            # 'statut_and_url': self.statut_and_url,
            }

        # return render(self.request, self.template_name, context=context)
        return context
    
    def post(self, request):
        user = request.user
        if 'lme' in request.POST:
            form = MajicForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.date_expiration_lme = add_years(datetime.today(), 1)
                instance.save()
                fileDeclaration = request.FILES['fileDeclaration']
                fileClausule = request.FILES['fileClausule']
                files = [
                    fileDeclaration,
                    fileClausule,
                ]
                url = instance.get_full_admin_url()
                send_demande_extraction_majic_lme(instance.user, 'LME', instance.organisation, url, files)

        return redirect('idgo_lme_majic:lme')
