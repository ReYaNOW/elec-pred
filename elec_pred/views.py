from typing import Any

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.base import TemplateView

from elec_pred.mixins import CustomMessageMixin


class IndexView(View):
    def get(
        self, request: HttpRequest, *_: Any, **__: Any
    ) -> HttpResponseRedirect:
        if request.user.is_authenticated:
            return redirect('/news')
        return redirect('/login')


class UserLoginView(CustomMessageMixin, LoginView):
    flash_message = _('Logged_in')
    message_type = 'success'

    template_name = 'users/login.html'
    form_class = AuthenticationForm


class UserLogoutView(CustomMessageMixin, LogoutView):
    flash_message = _('Logged_out')
    message_type = 'info'


class Error404View(TemplateView):
    template_name = 'errors/404.html'


class Error500View(TemplateView):
    template_name = 'errors/500.html'
