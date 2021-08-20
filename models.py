from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

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

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def get_full_admin_url(self):
        return settings.DOMAIN_NAME + self.get_admin_url()