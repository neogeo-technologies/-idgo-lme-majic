
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from idgo_lme_majic.views import MajicCreate
from idgo_lme_majic.views import LmeCreate

app_name = 'idgo_lme_majic'

router = DefaultRouter()

urlpatterns = [
   url('^majic/?$', MajicCreate.as_view(), name='majic'),
   url('^lme/?$', LmeCreate.as_view(), name='lme'),
  
]

urlpatterns += router.urls