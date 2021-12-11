# from django import forms
from django.contrib import messages
# from django.core import serializers
# from django.core.mail import EmailMessage, send_mail, BadHeaderError

from django.contrib.auth.decorators import login_required
# from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect  # , JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse  # , get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Userprofile
from .forms import ProfileForm


# USERPROFILES
class ProfilesListView(ListView):
    model = Userprofile
    template_name = 'userprofiles/all_profiles.html'
    context_object_name = 'userprofiles'
    paginate_by = 4

    # override the queryset method
    def get_queryset(self):
        # pylint: disable=maybe-no-member
        # queryset = Userprofile.objects.order_by('-created')
        return Userprofile.objects.order_by('-created').exclude(
            username=self.request.user)  # noqa: E501


# REGISTRATION FORMS


class NetworkProfileView(DetailView):
    model = Userprofile()
    template_name = 'userprofiles/profile_details.html'

    def get_user_profile(self, **kwargs):
        # pylint: disable=maybe-no-member
        pk = self. kwargs.get('pk')
        view_profile = Userprofile().objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        # pylint: disable=maybe-no-member
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
        profileform = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)  # noqa: E501
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
    # pylint: disable=maybe-no-member
    userprofile = Userprofile.objects.get(pk=pk)

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
    # pylint: disable=maybe-no-member
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
