from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from idgo_admin.exceptions import ExceptionsHandler
from idgo_admin.exceptions import ProfileHttp404
from idgo_admin.shortcuts import on_profile_http404

from idgo_admin import LOGIN_URL

from .majic import MajicCreate
from .lme import LmeCreate


__all__ = [
    MajicCreate,
    LmeCreate,
]

@ExceptionsHandler(ignore=[Http404], actions={ProfileHttp404: on_profile_http404})
@login_required(login_url=LOGIN_URL)
@csrf_exempt
def home(request, *args, **kwargs):
    return redirect(reverse('idgo_admin:list_my_datasets'))
