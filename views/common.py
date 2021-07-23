from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from django.views import View
from django.views.decorators.csrf import csrf_exempt
# from django.views.generic.base import TemplateView
# from django.views.generic.detail import SingleObjectMixin




DECORATORS = [csrf_exempt, login_required(login_url=settings.LOGIN_URL)]