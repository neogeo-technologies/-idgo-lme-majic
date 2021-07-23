from django.contrib import admin
from idgo_lme_majic.models import UserMajicLme
from django.contrib.auth import get_user_model
from idgo_lme_majic.filters import UserMajicLmeFilter
# Register your models here.

User = get_user_model()

class UserMajicLmeAdmin(admin.ModelAdmin):
  
    list_display = (
                    'user',
                    'majic',
                    'lme',
                    'date_expiration_majic',
                    'date_expiration_lme',
                    'organisation',
                    'get_territoire'
                    )
    list_filter = (
        (UserMajicLmeFilter),
        'majic',
        'lme',
        'organisation'
        )

    def get_territoire(self, obj):
        return obj.organisation.jurisdiction

    get_territoire.short_description = 'Territoire de compétence'

admin.site.register(UserMajicLme, UserMajicLmeAdmin)