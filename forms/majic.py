from django.contrib.gis import forms
from django.forms import HiddenInput
from django.forms.formsets import DELETION_FIELD_NAME
# from django.forms.models import BaseModelFormSet
# from django.utils import timezone

from idgo_lme_majic.models import UserMajicLme


class MajicForm(forms.ModelForm):

    majic = forms.BooleanField('MAJIC')

    date_expiration_majic = forms.DateField(
        label="Date d'expiration MAJIC", required=False)


    class Meta:
        model = UserMajicLme
        fields = [
            'user',
            'majic',
            'date_expiration_majic',
        ]
