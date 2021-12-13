from django.shortcuts import render  # , redirect, reverse, get_object_or_404
from userprofiles.models import Userprofile
from django.http import JsonResponse
from django.views.generic import (
    View,
)


# ALL USERS

def network(request):
    # A view to return the network page 

    return render(request, 'connect/network.html')


# CONTACTS

# @login_required
def my_contacts(request):
    # pylint: disable=maybe-no-member
    # profile = get_object_or_404(Userprofile, user=request.user)
    profile = Userprofile.objects.get(username=request.user)
    template = 'connect/my_contacts.html'

    context = {
        'profile': profile,
        # 'get_following': get_following,
        # 'get_followers': get_followers,
    }
    return render(request, template, context)


def my_followers(request):
    # A view to return the My Contacts page ""

    return render(request, 'connect/my_followers.html')


# @login_required
def following_ppl(request):
    # A view to return the My Contacts page
    # pylint: disable=maybe-no-member
    follow_ppl = Userprofile.objects.get(username=request.user)
    template = 'connect/my_contacts.html'

    context = {
        'follow_ppl': follow_ppl,
        # 'get_following': get_following,
        # 'get_followers': get_followers,
    }
    return render(request, template, context)


class ProfileData(View):
    def get(self, *args, **kwargs):
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
class ProfilesListView(ListView):
    model = Userprofile
    template_name = 'connect/all_profiles.html'
    context_object_name = 'userprofiles'

    # override the queryset method
    def get_queryset(self):
        queryset = Useprofile.objects.order_by('last_name')
        return Useprofile.objects.order_by('last_name').exclude(username=self.request.user)


class NetworkProfileView(DetailView):
    model = Useprofile
    template_name = 'userprofiles/profile_details.html'
    context_object_name = 'userprofiles'

    def get_user_profile(self, **kwargs):
        pk = self. kwargs.get('pk') 
        view_profile = Useprofile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super(NetworkProfileView, self).get_context_data(**kwargs)
        context['post_list'] = Useprofile.objects.filter(user__username__iexact=self.kwargs.get('username'))  # noqa: E501
        return context

    def get_user_profile(self, username):   
        return get_object_or_404(User, pk=username)
     #I know pk=username is not correct. I am not sure what to put pk=?

  # I was able to get the writers other posts using the code below. 
  # I did not have to show this code for this question. 
  # But just to show you that the pk above has to be username. 
  # Or Else the code below won't work(I guess)        
    def get_context_data(self, **kwargs):
        context = super(NetworkProfileView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.filter(user__username__iexact=self.kwargs.get('username'))  # noqa: E501
        return context


# @login_required
def all_profiles(request):
    # pylint: disable=maybe-no-member
    all_profiles = Userprofile.objects.all()
    print(all_profiles)
    # print(all_profiles[0]['username'])
    template = 'connect/network.html'
    context = {
        'all_profiles': all_profiles,
    }
    return render(request, template, context)


class UserDetailView(DetailView):
    model = Userprofile


def myContacts(request):
    # A view to return the My Contacts page

    return render(request, 'connect/my_contacts.html')

"""
