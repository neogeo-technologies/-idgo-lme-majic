from django.contrib.admin.filters import SimpleListFilter
from idgo_lme_majic.models import UserMajicLme

class UserMajicLmeFilter(SimpleListFilter):
    template = 'admin/idgo_lme_majic/dropdown_filter.html'

    # Filter title
    title = "User"

    # url param
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        return UserMajicLme.objects.all().values_list('user', 'user__username').distinct()

    def queryset(self, request, queryset):
        # Si filtre il y'a
        if self.value():
            return queryset.filter(
                user=self.value()
            )

        return queryset