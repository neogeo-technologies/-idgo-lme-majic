from django.contrib.gis import forms

from django.forms.formsets import DELETION_FIELD_NAME
# from django.forms.models import BaseModelFormSet
# from django.utils import timezone

from idgo_lme_majic.models import UserMajicLme


class LmeForm(forms.ModelForm):

    lme = forms.BooleanField('LME')

    date_expiration_lme = forms.DateField(
        label="Date d'expiration LME")


    class Meta:
        model = UserMajicLme
        fields = [
            'majic',
            'date_expiration_lme',
        ]
