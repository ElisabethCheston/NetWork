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


class UserprofileAdmin(admin.ModelAdmin):
    """ Membership Information """
    list_display = (
        'first_name',
        'last_name',
        'username',
        'created',
        'title',
        'company_name',
        'industry',
        'country',
        'city',
        'employment',
        'purpose',
    )

    ordering = ('created',)


admin.site.register(Membership, MembershipAdmin)
admin.site.register(Userprofile, UserprofileAdmin)
admin.site.register(Industry)
admin.site.register(Profession)
admin.site.register(Purpose)
admin.site.register(Business)
admin.site.register(Employment)
admin.site.register(Status)
