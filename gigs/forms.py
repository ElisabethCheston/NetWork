# from django.contrib.auth.models import User
from django import forms
from .models import Gig
# from userprofiles.models import Userprofile, Industry, Profession


class GigForm(forms.ModelForm):

    class Meta:
        model = Gig
        fields = [
            'title',
            'industry',
            'city',
            'country',
            'position',
            'overview',
            'requirements',
            'contact',
            'deadline',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Title'}),
            'industry': forms.Select(attrs={
                'class': 'form-control', 'placeholder': 'Industry'}),
            'profession': forms.Select(attrs={
                'class': 'form-control', 'placeholder': 'Profession'}),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'City'}),
            'country': forms.Select(attrs={
                'class': 'form-control', 'placeholder': 'Country'}),
            'position': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Job Position (250 characters)'}),  # noqa: E501
            'overview': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Company Summary (250 characters)'}),  # noqa: E501
            'requirements': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Job Requirements (250 characters)'}),  # noqa: E501
            'contact': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': '"Send you CV and cover letter to.."'}),  # noqa: E501
            'deadline': forms.DateInput(
                format=('%Y-%m-%d'), attrs={
                    'class': 'form-control',
                    'placeholder': 'Deadline Date',
                    'type': 'date'
                }),
        }
