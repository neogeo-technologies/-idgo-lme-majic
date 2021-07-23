from django.conf import settings

from django.db import models
from idgo_admin.models import Organisation

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class UserMajicLme(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    majic = models.BooleanField('MAJIC', default=False)
    
    lme = models.BooleanField('LME', default=False)

    date_expiration_majic = models.DateField("Date d'expiration MAJIC", null=True, blank=True)

    date_expiration_lme = models.DateField("Date d'expiration LME", null=True, blank=True)

    organisation = models.ForeignKey(
        'idgo_admin.Organisation', models.CASCADE, db_column='organisation', related_name='organisation',  default=False)
