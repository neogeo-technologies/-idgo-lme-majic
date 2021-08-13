from idgo_admin.models.organisation import Organisation

from django.contrib.gis import forms
from django.forms import HiddenInput
from django.forms.formsets import DELETION_FIELD_NAME
# from django.forms.models import BaseModelFormSet
# from django.utils import timezone
from django.shortcuts import get_object_or_404

from idgo_lme_majic.models import UserMajicLme


class MajicForm(forms.ModelForm):

    class Meta:
        model = UserMajicLme
        fields = [
            'user',
            'organisation',
        ]
    
    def __init__(self, *args, **kwargs):
        super(MajicForm, self).__init__(*args, **kwargs)