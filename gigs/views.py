

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404  # , redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse  # , HttpResponse
# from django.db.models import Q
# from django.contrib import messages
from django.urls import reverse_lazy
# from django.db.models.functions import Lower
from django.core import serializers
# from django.views.decorators.http import require_http_methods

from django.views.generic import (
    # TemplateView,
    View,
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)
from userprofiles.models import Userprofile  # , Membership
from .models import Gig
from .forms import GigForm


# ALL GIGS

class GigListView(ListView):
    model = Gig
    template_name = 'gigs/gig.html'
    context_object_name = 'gigs'
    paginate_by = 3
    ordering = ['-created']


class GigDetailView(DetailView):
    model = Gig


"""
def get(self, request, gig_pk, *args, **kwargs):
    gig_qs = Gig.objects.filter(pk=gig_pk)
    if gig_gs.exists():
        gig = gig_qs.first()

    usermembership = UserMembership.objectsfilter(user=request.user).first()
    usermembership_type = usermembership.membership.membership_type

    gig_allowed_mem_type = gig.allowed_membership.all()

    context = {
        'object': None
    }
    if gig_allowed_mem_type.filter(
        membership_type=usermembership_type).exists():

        return render(request, 'create_gigs.html', context)
"""

# userprofile GIGS

@login_required
def my_gigs(request):
    # pylint: disable=maybe-no-member
    profile = Userprofile.objects.get(username=request.user)
    template = 'gigs/my_gigs.html'
    context = {
        'profile': profile,
    }
    return render(request, template, context)


class NewGigListView(ListView):
    model = Gig
    template_name = 'gigs/new_gig.html'
    context_object_name = 'gigs'
    ordering = ['-created']
    paginate_by = 5


class GigCreateView(LoginRequiredMixin, CreateView):
    model = Gig
    form_class = GigForm
    template_name = 'gigs/create_gig.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.userprofile
        return super().form_valid(form)


class GigUpdateView(LoginRequiredMixin, UpdateView):  # UserPassesTestMixin
    model = Gig
    form_class = GigForm
    template_name = 'gigs/create_gig.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.userprofile
        return super().form_valid(form)

    def test_func(self):
        gig = self.get_object()
        if self.request.user == gig.author:
            return True
        return False


class GigDeleteView(LoginRequiredMixin, DeleteView):  # UserPassesTestMixin
    model = Gig
    success_url = reverse_lazy('my_gigs')


# CHOICE FOR GIGS
class GigsData(View):
    def get(self, *args, **kwargs):
        # pylint: disable=maybe-no-member
        add_gig = Gig.objects.get(user=self.request.user)
        qs = add_gig.get_proposal_contact()
        gd_list = []
        for user in qs:
            # Select random profiles
            # p = Gig.objects.get(user__username=user.username)
            p = get_object_or_404(Gig, user__username=user.username)
            gig_item = {
                # 'id': p.id,
                'author': p.user.username,
                'title': p.user.username,
                'firstname': p.firstname,
                'lastname': p.lastname,
                'avatar': p.avatar.url,
                'profession': p.profession,
                'company_name': p.company_name,
                'industry': p.obj.industry,
                'liked': p.obj.liked,
                'gigdescription': p.obj.gigdescription,
                'extrainfo': p.obj.extrainfo,
                'deadline': p.obj.deadline,
                'updated': p.obj.updated,
                'created': p.obj.created,
                'city': p.obj.city,
                'country': p.obj.country,
            }
            gd_list.append(gig_item)
        return JsonResponse({'pf_data': gd_list})


def gig_json(request):
    # pylint: disable=maybe-no-member
    qs = Gig.objects.all()
    data = serializers.serialize('json', qs)
    context = {
        'data': data,
    }
    return JsonResponse(context)
