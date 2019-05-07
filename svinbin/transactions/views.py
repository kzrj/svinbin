# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from django.http import HttpResponse



class CreateDisposalEvent(TemplateView):
	template_name = "index.html"
    
		