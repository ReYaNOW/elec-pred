from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from elec_pred.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'plot_number',
        'residents',
        'last_login',
    )
    list_filter = (('date_joined', DateFieldListFilter),)
    search_fields = ['plot_number']
