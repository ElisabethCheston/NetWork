"""
from django.contrib import admin
from userprofiles.models import Membership


class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        'membership_type',
        'price',
        'stripe_price_id',
    )

    ordering = ('membership_type',)


admin.site.register(Membership, MembershipAdmin)
"""
