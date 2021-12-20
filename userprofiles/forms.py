from .models import Userprofile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit, Layout, Row, Column
# from crispy_forms.bootstrap import InlineRadios, FormActions


# REGISTRATION USER FORM


class UserprofileCreationForm(forms.Form):

    first_name = forms.CharField(label='First Name', min_length=2, max_length=50)  # noqa: E501
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=50)  # noqa: E501)
    username = forms.CharField(label='Enter email', min_length=4, max_length=150)  # noqa: E501
    email = forms.EmailField(label='Confirm email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)  # noqa: E501
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  # noqa: E501
    # terms = forms.BooleanField(label="Terms & Conditions", required=True)  # noqa: E501

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Email already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        if commit:
            user.save()
        return user


"""
class UserprofileCreationForm(forms.Form):

    first_name = forms.CharField(label='First Name', min_length=2, max_length=50)  # noqa: E501
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=50)  # noqa: E501)
    username = forms.CharField(label='Enter email', min_length=4, max_length=150)  # noqa: E501
    email = forms.EmailField(label='Confirm email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)  # noqa: E501
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  # noqa: E501
    # terms = forms.BooleanField(label="Terms & Conditions", required=True)  # noqa: E501

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]


def clean_terms(self):
        terms = self.cleaned_data['terms'].lower()
        r = User.objects.filter(terms=terms)
        if r.count():
            raise ValidationError("You must accept the terms and conditions")
        return


    first_name = forms.CharField(label='First Name', min_length=2, max_length=50)  # noqa: E501
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=50)  # noqa: E501)
    username = forms.CharField(label='Enter email', min_length=4, max_length=150)  # noqa: E501
    email = forms.EmailField(label='Confirm email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)  # noqa: E501
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  # noqa: E501

    def save(self, commit=True):
        user = super(UserprofileCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        # user.terms = self.cleaned_data['terms']
        if commit:
            user.save()
        return user


def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name'],
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class RegisterUserForm(UserCreationForm):
    agree = forms.BooleanField(
        widget=forms.RadioSelect,
        required=True,
        initial=True
        )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {
            'novalidate'
        }
        self.helper.layout = Layout(
            Row(
                Column('first_name'),
                Column('last_name'),
                Column('username'),
                Column('email'),
                Column('password1'),
                Column('password2')
            ),
            InlineRadios('agree'),
            FormActions(
                Submit('save_profile', 'Save Profile')
            )
        )

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class TermsForm(forms.ModelForm):
    class Meta:
        model = TermUser
        fields = [
            'agree',
        ]

        widgets = {
            'agree': CheckboxInput(attrs={'class': 'agree'}),
        }
"""

# -- EDIT FORM IN PROFILE -- #


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = [
            'avatar',
            'picture',
            'title',
            'company_name',
            'industry',
            'description',
            'country',
            'city',
            'locations',
            'employment',
            'business',
            'purpose',
        ]

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.country = self.cleaned_data['country']
        user.city = self.cleaned_data['city']
        user.locations = self.cleaned_data['locations']
        if commit:
            user.save()
        return user
