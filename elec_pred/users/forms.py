from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

username_validator = RegexValidator(
    r'^[a-zA-Z0-9@/./+/-/_]*', _('user_name_validation_error')
)

User = get_user_model()


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_('passwd_help_message'),
    )

    plot_number = forms.CharField(
        label=_('Plot Number'),
        max_length=100,
        required=True,
        help_text=_('enter_plot_number'),
    )

    residents = forms.CharField(
        label=_('Residents'),
        max_length=255,
        required=False,
        help_text=_('who_lives_there'),
    )

    class Meta:
        model = User
        fields = [
            'plot_number',
            'residents',
            'username',
            'password1',
            'password2',
        ]

        labels = {
            'username': _('Nickname'),
            'password1': _('Password'),
        }
        widgets = {
            'username': forms.TextInput(
                attrs={'autofocus': False, 'required': True}
            )
        }

        help_texts = {'username': _('username_help_message')}

        error_messages = {
            'username': {
                'unique': _('user_exists_message'),
            },
        }

        validators = {'username': username_validator}

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # Убираем placeholder из всех полей
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ''


class UserUpdateForm(UserCreateForm):
    def clean_username(self) -> str:
        return self.cleaned_data.get('username')
