from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from elec_pred.mixins import (
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
    ProtectedErrorHandlerMixin,
)

from .forms import UserCreateForm, UserUpdateForm

User = get_user_model()


class UserListView(ListView):
    template_name = 'users/users_list.html'

    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'crud_parts/create.html'
    extra_context = {
        'title': _('Sign Up'),
        'button_text': _('Sign up'),
    }

    model = User
    form_class = UserCreateForm

    success_url = reverse_lazy('login')
    success_message = _('Sign up success')


class UserUpdateView(
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change user')}

    model = User
    form_class = UserUpdateForm

    success_url = reverse_lazy('users_list')
    success_message = _('Edit success')

    permission_url = reverse_lazy('users_list')
    permission_message = _('Dont have permissions to change')


class UserDeleteView(
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
    SuccessMessageMixin,
    ProtectedErrorHandlerMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting user')}

    model = User

    success_url = reverse_lazy('users_list')
    success_message = _('Delete success')

    permission_url = reverse_lazy('users_list')
    permission_message = _('Dont have permissions to change')

    protected_url = reverse_lazy('users_list')
    protected_message = _('protected_user')
