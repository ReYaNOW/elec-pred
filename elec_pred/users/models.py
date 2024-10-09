from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(
        verbose_name='email address', blank=True, null=True
    )

    plot_number = models.CharField(
        max_length=100, verbose_name='Номер участка', unique=True
    )
    residents = models.CharField(
        max_length=255,
        verbose_name='Кто живет на участке',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'Участок №{self.plot_number}'
