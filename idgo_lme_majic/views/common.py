from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



DECORATORS = [csrf_exempt, login_required(login_url=settings.LOGIN_URL)]