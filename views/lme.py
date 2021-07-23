from django.shortcuts import render

from idgo_lme_majic.forms import MajicForm
from idgo_lme_majic.models import UserMajicLme
from django.utils.decorators import method_decorator
from idgo_lme_majic.views.common import DECORATORS
from django.views.generic.edit import CreateView

# Create your views here.


@method_decorator(DECORATORS, name='dispatch')
class LmeCreate(CreateView):

    model = UserMajicLme

    form_class = MajicForm

    template_name = 'idgo_lme_majic/lme/lme.html'