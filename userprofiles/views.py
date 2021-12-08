from .models import Userprofile
from django import forms
from django.contrib import messages
from .forms import ProfileForm, RegisterUserForm, TermsForm
from django.core import serializers
from django.core.mail import EmailMessage, send_mail, BadHeaderError
# from django.core.paginator import Paginator
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
# from django.db.models.functions import Lower
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView


# PASSWORD USAGE

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    # template_name = 'userprofiles/password_change.html'
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('profile_details')


def PasswordSuccess(request):
    return render(request, 'userprofiles/password_success.html', {})


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'userprofiles/password_reset_done.html'


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "profileusers/password_reset_email.txt"  # noqa: E501
                    c = {
                        "email": user.email,
                        'domain': 'https://biz-net.herokuapp.com',
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
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(
        request=request, template_name="profileusers/password_reset.html", context={  # noqa: E501
            "password_reset_form": password_reset_form})  # noqa: E501


# REGISTER AN ACCOUNT

def Register(request):
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
    return render(request, 'userprofiles/register.html', context)


def terms(request):
    # pylint: disable=maybe-no-member
    template = 'userprofiles/terms.html'

    return render(request, template)


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
    template = 'userprofiles/login_register_page.html'
    context = {}
    return render(request, template, context)



# USERPROFILES

class ProfilesListView(ListView):
    model = Userprofile
    template_name = 'userprofiles/all_profiles.html'
    context_object_name = 'userprofiles'
    paginate_by = 4

    # override the queryset method
    def get_queryset(self):
        queryset = Userprofile.objects.order_by('-created')
        return Userprofile.objects.order_by('-created').exclude(
            username=self.request.user)  # noqa: E501


class NetworkProfileView(DetailView):
    model = Userprofile()
    template_name = 'userprofiles/profile_details.html'

    def get_user_profile(self, **kwargs):
        pk = self. kwargs.get('pk') 
        view_profile = Userprofile().objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        user_profile = Userprofile().objects.get(username=self.request.user)
        if view_profile.username in user_profile.following.all():
            follow = True
        else:
            follow = False

        context['follow'] = follow
        return context

    def get_success_url(self):
        return reverse(
            'events:profile_details', kwargs={'pk': self.object.profile_id})


def profile_details(request):
    # pylint: disable=maybe-no-member
    profile = Userprofile.objects.get(username=request.user)
    template = 'userprofiles/profile_details.html'
    context = {
        'profile': profile,
    }
    return render(request, template, context)


def profile_edit(request):
    if request.method == 'POST':
        profileform = ProfileForm(request.POST,
                                request.FILES,
                                instance=request.user.userprofile)
        if profileform.is_valid():
            profileform.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile_details')
        else:
            messages.error(
                request, 'Update failed. Please check if your inputs are valid.')  # noqa: E501
    else:
        profileform = ProfileForm(instance=request.user.userprofile)
    context = {
        'profileform': profileform,
    }
    return render(request, 'userprofiles/profile_edit.html', context)


def profile_delete(request, pk):
    userprofile = User.objects.get(pk=pk)

    if request.method == "POST" and request.user.username == userprofile:
        userprofile.delete()
        messages.success(request, "Account has been successfully deleted!")
        return HttpResponseRedirect(reverse('userprofiles'))

    context = {
        'userprofile': userprofile,
        }
    return render(request, 'userprofiles/user_confirm_delete.html', context)


@login_required
def follow_unfollow_profile(request):
    if request.method == 'POST':
        user_profile = Userprofile.objects.get(username=request.user)
        pk = request.POST.get('profile_pk')
        userprofile = Userprofile.objects.get(pk=pk)

        if userprofile.username in user_profile.following.all():
            user_profile.following.remove(userprofile.username)
        else:
            user_profile.following.add(userprofile.username)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('all_profiles')
