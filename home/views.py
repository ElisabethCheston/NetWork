from userprofiles.models import Userprofile

from django import forms
from django.urls import reverse_lazy

from django.core import serializers
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login #, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.db.models.functions import Lower
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from userprofiles.forms import ProfileForm, RegisterUserForm, TermsForm



# STARTING PAGE
def index(request):
    return render(request, 'home/index.html')


# PASSWORD USAGE
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


def PasswordSuccess(request):
    return render(request, 'home/password_success.html', {})


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'home/password_reset_done.html'


"""
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "home/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'https://network-jobs.herokuapp.com',
                        'site_name': 'NetWork',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, [user.email], fail_silently=True)  # noqa: E501
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')  # noqa: E501
                    return redirect("main:homepage")
            messages.error(request, 'An invalid email has been entered.'
    password_reset_form = PasswordResetForm()
    return render(request, "home/password_reset.html", context)
"""

# REGISTER AN ACCOUNT

def register(request):
    # pylint: disable=maybe-no-member
    form = RegisterUserForm()
    termform = TermsForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        termform = TermsForm(request.POST)
        if form.is_valid() and termform.is_valid():
            form.save()
            termform.save(commit=False)
            user = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login_register_page')
    else:
        form = RegisterUserForm()
        termform = TermsForm()
        messages.warning(request, 'Your account cannot be created.')

    context = {
        'form': form,
        'termform': termform
    }
    return render(request, 'home/register.html', context)


def terms(request):
    # pylint: disable=maybe-no-member
    template = 'home/terms.html'

    return render(request, template)


# REGISTRATION FORMS
@login_required
def Profile(request):
    # profile_form1 = ProfileForm1()
    if request.method == 'POST':
        profile = Profile(request.POST,
                                request.FILES,
                                instance=request.user.userprofile)
        if profile.is_valid():
            profile.save()
            # messages.success(request, 'Step 1 of 3 done of creating your profile!')
            return redirect('profie_edit')
        # else:
            # messages.error(request, 'Update failed. Please check if your inputs are valid.')
    else:
        profile = Userprofile.objects.create(username=request.user)
        # profile_form1 = ProfileForm1(instance=request.user.profileuser)
        # return redirect('register_1')
    context = {
        'profile': profile,
    }
    return render(request, 'userprofiles/profile.html', context)
   

# SINGIN TO ACCOUNT
def loginPage(request):
    if request.method == 'POST':
        # Connected to the name field in the login_page.
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all_profiles')
        else:
            messages.info(request, 'Username or Password is incorrect!')
            return redirect('login_page')

    template = 'home/login_page.html'
    context = {}
    return render(request, template, context)


# VERTIFY USER ACCOUNT
def loginRegisterPage(request):
    if request.method == 'POST':
        # Connected to the name field in the login_register_page.
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username or Password is incorrect!')

    template = 'home/login_register_page.html'
    context = {}
    return render(request, template, context)


# SINGIN TO ACCOUNT
def loginPage(request):
    if request.method == 'POST':
        # Connected to the name field in the login_page.
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all_profiles')
        else:
            messages.info(request, 'Username or Password is incorrect!')
            return redirect('login_page')

    template = 'home/login_page.html'
    context = {}
    return render(request, template, context)


"""
def login(request):
    return render(request, 'home/login.html')


def logout(request):
    return render(request, 'home/logout.html')
"""