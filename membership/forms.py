
from django.contrib.auth.models import User
from django import forms
from profileusers.models import Profileuser, Membership


class MembershipForm(forms.ModelForm):

    class Meta:
        model = Membership
        fields = [
            'slug',
            'membership_type',
            'stripe_price_id',
            'price',            
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserMembershipForm(forms.ModelForm):

    class Meta:
        model = Profileuser
        fields = [
            'username',
            'stripe_customer_id',
            'membership',
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

