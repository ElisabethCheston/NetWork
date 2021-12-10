from django.contrib import admin
from .models import Gig


class GigAdmin(admin.ModelAdmin):
    """ Membership Information """
    list_display = (
        'title',
        'industry',
        'city',
        'country',
        'position',
        'overview',
        'requirements',
        'contact',
        'deadline',
    )

    ordering = ('title',)


admin.site.register(Gig, GigAdmin)
