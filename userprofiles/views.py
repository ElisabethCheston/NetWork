# from django.core.paginator import Paginator
# from django.conf import settings
import json
from django.contrib import messages
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, UserCreationForm  # noqa: E501
# from django.db.models.functions import Lower
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# from django.core import serializers
from django.core.mail import send_mail, BadHeaderError  # EmailMessage
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Userprofile
from .forms import ProfileForm, UserprofileCreationForm  # TermsForm


# PASSWORD USAGE


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


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
                    email_template_name = "userprofiles/password_reset_email.txt"  # noqa: E501
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
            messages.error(request, 'An invalid email has been entered.')
        password_reset_form = PasswordResetForm()
    return render(request=request, template_name="userprofiles/password_reset.html", context={"password_reset_form": password_reset_form})  # noqa: E501


# REGISTER AN ACCOUNT

def Register(request):
    if request.method == 'POST':
        f = UserprofileCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('login_register_page')

    else:
        f = UserprofileCreationForm()

    context = {
        'form': f,
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
            return redirect('profile_edit')
        else:
            messages.info(request, 'Username or Password is incorrect!')

    template = 'userprofiles/login_register_page.html'
    context = {}
    return render(request, template, context)


@login_required
def Profile(request):
    profile = Userprofile(request.POST, request.FILES, instance=request.user)  # noqa: E501
    return redirect('profile_details')

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

    template = 'userprofiles/login_page.html'
    context = {}
    return render(request, template, context)


# USERPROFILE


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


class ProfilesListView(ListView):
    model = Userprofile
    template_name = 'userprofiles/all_profiles.html'
    context_object_name = 'userprofiles'
    paginate_by = 4


"""
    # override the queryset method
    def get_queryset(self):
        queryset = Userprofile.objects.order_by('-created')
        return Userprofile.objects.order_by('-created').exclude(username=self.request.user)  # noqa: E501
"""


class NetworkProfileView(DetailView):
    model = Userprofile
    template_name = 'userprofile/profile_details.html'
    # context_object_name = 'userprofile'

    def get_user_profile(self, **kwargs):
        pk = self. kwargs.get('pk')
        view_profile = Userprofile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        user_profile = Userprofile.objects.get(username=self.request.user)
        if view_profile.username in user_profile.following.all():
            follow = True
        else:
            follow = False

        context['follow'] = follow
        return context

    def get_success_url(self):
        return reverse('events:profile_details', kwargs={'pk': self.object.profile_id})  # noqa: E501


# @login_required
def create_customer(request):
    # pylint: disable=maybe-no-member
    if request.method == 'POST' and request.is_ajax():
        form = ProfileForm(request.POST)  # noqa: E501
        resp = {}
        if form.is_valid():
            form.save()
            resp['success'] = True
        else:
            resp['success'] = False
            csrf_context = {}
            csrf_context.updated(csrf(request))
            profileForm_html = render_crispy_form(form, context=csrf_context)  # noqa: E501
            resp['html'] = profileForm_html
        return HttpResponse(json.dumps(resp), content_type='application/json')

    form = ProfileForm()
    template = 'userprofiles/costumer_form.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def profile_details(request):
    # pylint: disable=maybe-no-member
    if request.method == 'POST':
        profile = Userprofile.objects.all(username=request.user)
        if profile.is_valid():
            profile.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile_details')
    else:
        profile = Userprofile.objects.all()
        # profile = Userprofile.objects.get(username=request.user)
    template = 'userprofiles/profile_details.html'
    context = {
        'profile': profile,
    }
    return render(request, template, context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        profileform = ProfileForm(request.POST, request.FILES, instance=request.user)  # noqa: E501
        if profileform.is_valid():
            profileform.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile_details')
        else:
            messages.error(request, 'Update failed. Please check if your inputs are valid.')  # noqa: E501
    else:
        profileform = ProfileForm(instance=request.user)
    template = 'userprofiles/profile_edit.html'
    context = {
        'profileform': profileform,
    }
    return render(request, template, context)


def profile_delete(request, pk):
    userprofile = User.objects.get(pk=pk)

    if request.method == "POST" and request.user.username == userprofile:
        userprofile.delete()
        messages.success(request, "Account has been successfully deleted!")
        return HttpResponseRedirect(reverse('home'))

    context = {
        'userprofile': userprofile,
        }
    return render(request, 'userprofiles/user_confirm_delete.html', context)



def profile_delete(request, pk):
    userprofile = User.objects.get(pk=pk)

    if request.method == "POST" and request.user.username == userprofile:
        userprofile.delete()
        messages.success(request, "Account has been successfully deleted!")
        return HttpResponseRedirect(reverse('home'))

    context = {
        'userprofile': userprofile,
        }
    return render(request, 'userprofiles/user_confirm_delete.html', context)


"""
# USERPROFILE GIGS

@login_required
def my_gigs(request):
    # pylint: disable=maybe-no-member
    profile = Userprofile.objects.get(username=request.user)
    template = 'userprofiles/my_gigs.html'
    context = {
        'profile': profile,
    }
    return render(request, template, context)

    
@login_required
def create_gig(request):
    # pylint: disable=maybe-no-member
    model = gigs.model.gig
    # if request.method == 'POST':
        # create_usergig = get_object_or_404(Gig, username=request.username)
    gigform = GigForm # (request.POST, instance=request.username.gig)
    template = 'userprofiles/create_gigs.html'

    # else:
        # gigform = GigForm(instance=request.user.gig)
    # context = {'gigform': gigform,}
    return render(request, template)
"""

"""
    #if request.method == 'POST':
    gigform = GigForm(request.POST or None, request.FILES or None)
    g = Gig.objects.get(pk=1)
    response = serializers.serialize('python', [g], ensure_ascii=False)
    context = {
        'gigform': gigform,
    }
    return render(request, 'userprofiles/create_gig.html', context)

    if gigform.is_valid():
        gigform.save()
        messages.success(request, 'Your Gig has been updated!')
        return redirect('my_gigs')
        # else:
            # messages.error(request, 'Update failed. Please check if your inputs are valid.')  # noqa: E501
    # else:
        # gigform = gigform()
        """


# SUGGEST BUTTON OF PPL TO FOLLOW

# class for random contacts to add
"""
class MyProfile(TemplateView):
    template_name = 'userprofiles/profile_details.html'


class ProfileData(View):
    def get(self, *args, **kwargs): # , *args, **kwargs
        # pylint: disable=maybe-no-member
        profile = Userprofile.objects.get(user=self.request.user)
        qs = profile.get_proposal_contact()
        profile_to_follow_list = []
        for user in qs:
            # Select random profiles
            p = Userprofile.objects.get(user__username=user.username)
            # p = get_object_or_404(Userprofile, user__username=user.username)
            profile_item = {
                # 'id': p.id,
                'user': p.user.username,
                'firstname': p.firstname,
                'lastname': p.lastname,
                'avatar': p.avatar.url,
                'profession': p.profession,
                'company_name': p.company_name,
            }
            profile_to_follow_list.append(profile_item)
        return JsonResponse({'pf_data': profile_to_follow_list})
"""
