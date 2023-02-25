from django.contrib import admin
from .models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display=(
        'ticker',
        'name',
        'sector',
        'industry',

    )

    list_filter = (
        'sector',
        'industry',
    )

admin.site.register(Company, CompanyAdmin)
