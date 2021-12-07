from django.contrib import admin
from .models import (
    Userprofile,
    Employment,
    Status,
    Industry,
    Profession,
    Purpose,
    Business,
    Membership,
)


class MembershipAdmin(admin.ModelAdmin):
    """ Membership Information """
    list_display = (
        'membership_type',
        'price',
        'stripe_price_id',
    )

    ordering = ('membership_type',)


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Userprofile)
admin.site.register(Industry)
admin.site.register(Profession)
admin.site.register(Purpose)
admin.site.register(Business)
admin.site.register(Employment)
admin.site.register(Status)
