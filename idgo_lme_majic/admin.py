from django.contrib import admin
from idgo_lme_majic.models import UserMajicLme
from django.contrib.auth import get_user_model
from idgo_lme_majic.filters import UserMajicLmeFilter
# Register your models here.

User = get_user_model()
def remove_registre(modeladmin, request, queryset):
    for e in queryset:

        e.delete()
remove_registre.short_description = "Supprimer registre MAJIC/LME"

def to_majic(modeladmin, request, queryset):
    # for e in queryset:
    queryset.update(majic=True)
to_majic.short_description = "Valider demande MAJIC"

def to_lme(modeladmin, request, queryset):
    queryset.update(lme=True)
to_lme.short_description = "Valider demande LME"


class UserMajicLmeAdmin(admin.ModelAdmin):
    actions = [remove_registre, to_majic, to_lme]
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