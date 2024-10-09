from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        if not request.user.is_authenticated:
            messages.error(request, _('Arent authorized'))
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class CustomPermissionRequiredMixin(UserPassesTestMixin):
    permission_url: str = None
    permission_message: str = None

    def test_func(self) -> bool:
        return self.get_object() == self.request.user

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class CustomMessageMixin:
    """Add a custom type message on successful page."""

    flash_message: str = ''
    message_type: str = ''

    def get_success_url(self) -> str:
        success_url = super().get_success_url()
        getattr(messages, self.message_type)(self.request, self.flash_message)
        return success_url

    def get_flash_message(self, cleaned_data: dict[str, Any]) -> str:
        return self.flash_message % cleaned_data


class ProtectedErrorHandlerMixin:
    protected_message = None
    protected_url = None

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
