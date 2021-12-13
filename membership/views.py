from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from userprofiles.models import Userprofile, Industry, Profession, Membership, Employment, Status, Membership  # noqa: E501

from gigs.models import Gig
from bag.contexts import bag_contents
from userprofiles.forms import ProfileForm

# from checkout.models import Subscription
# from checkout.forms import SubscriptionForm

# import stripe
# import json
# stripe.api_key = settings.STRIPE_SECRET_KEY


"""
Reference:
https://github.com/sunilale0/django-stripe-subscription
https://stripe.com/docs/billing/integration-builder
"""

# -- STRIPE -- #
"""
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=True)
"""

# -- MEMBERSHIP -- #


def all_membership(request):
    # A view to show all products

    products = Membership.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'membership/membership_list.html', context)


def membership_detail(request, product_id):

    # A view to show individual membership details
    product = get_object_or_404(Membership, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'membership/membership_detail.html', context)


def get_usermembership(request):
    usermembership = Userprofile().objects.get(user='user')
    if usermembership.exists():
        return usermembership.first()
    return None


def get_user_subscription(request):
    user_subscription = Subscription.objects.filter(
        usermembership = get_usermembership(request))
    if user_subscription.exists():
        user_subscription = user_subscription.first()
        return user_subscription
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class MembershipSelectView(LoginRequiredMixin, ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_usermembership(self.request)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        selected_membership = request.POST.get('membership_type')
        usermembership = get_usermembership(request)
        # user_subscription = get_user_subscription(request)
        selected_membership_qs = Membership.objects.filter(
            membership_type = selected_membership)
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()

           # -- Validation -- #
        if usermembership.membership == selected_membership:
            if usermembership != Free:
                messages.info(request, "You already have this membership.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        request.session['bag'] = selected_membership.membership_type # selected_membership_type  # noqa: E501

        return HttpResponseRedirect(reverse('payment'))


@login_required
def add_product(request):
    # Add a product to the store
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('select'))

    if request.method == 'POST':
        form = MembershipForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = MembershipForm()

    template = 'membership/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    # Edit a product in the store
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('select'))

    product = get_object_or_404(Membership, pk=product_id)
    if request.method == 'POST':
        form = MembershipForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = MembershipForm(instance=product)
        messages.info(request, f'You are editing {product.membership_type}')

    template = 'membership/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    # Delete a product from the store
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('select'))

    product = get_object_or_404(Membership, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def updateTransactionRecords(request):
    usermembership = get_usermembership(request)
    selected_membership = get_selected_membership(request)
    usermembership.membership = selected_membership
    usermembership.save()

    sub, created = Subscription.objects.get_or_create(
        usermembership=usermembership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(
        selected_membership))
    return redirect(reverse('select'))


# -- PROFILEUSER INFO -- #

    # usermembership = get_usermembership(request)
    # selected_membership = get_selected_membership(request)

def membership_profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(Useprofile, username=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    """
    if request.method == 'POST':
        form = UserMembershipForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')  # noqa: E501
    else:
        form = UserMembershipForm(instance=profile)
    """
    # orders = profile.orders.all()

    template = 'membership/membership_profile.html'
    context = {
        # 'form': form,
        'profile': profile,
        # 'on_profile_page': True,
        # 'membership_type': membership_type,
    }
    return render(request, template, context)


"""
@login_required
def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type='Free')
    usermembership = get_usermembership(request)
    usermembership.membership = free_membership
    usermembership.save()

    messages.info(
        request, "Successfully cancelled membership. We have sent an email")
    # sending an email here

    return redirect(reverse('memberships:select'))


# -- PAYMENT HISTORY -- #

def payment_history(request):
    membership = Membership.objects.all()
    template = 'membership/payment_history.html'
    context = {
        'membership': membership
    }
    return render(request, template, context)

"""
# -- SUBSCRIPTION RESPONCES -- #


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


# -- ADMIN   -- #
@login_required
def add_membership(request):
    # Add a membership to the store
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('network'))

    if request.method == 'POST':
        form = MembershipForm(request.POST, request.FILES)
        if form.is_valid():
            membership = form.save()
            messages.success(request, 'Successfully added membership!')
            return redirect(reverse('membership_detail', args=[membership.id]))
        else:
            messages.error(request, 'Failed to add membership. Please ensure the form is valid.')  # noqa: E501
    else:
        form = MembershipForm()

    template = 'membership/add_membership.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_membership(request, membership_id):
    # Edit a membership in the store
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('network'))

    membership = get_object_or_404(Membership, pk=membership_id)
    if request.method == 'POST':
        form = MembershipForm(request.POST, request.FILES, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated membership!')
            return redirect(reverse('membership_detail', args=[membership.id]))
        else:
            messages.error(request, 'Failed to update membership. Please ensure the form is valid.')  # noqa: E501
    else:
        form = MembershipForm(instance=membership)
        messages.info(request, f'You are editing {membership.name}')

    template = 'membership/edit_membership.html'
    context = {
        'form': form,
        'membership': membership,
    }

    return render(request, template, context)


@login_required
def delete_membership(request, membership_id):
    # Delete a membership from the store
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('select'))

    membership = get_object_or_404(Membership, pk=membership_id)
    membership.delete()
    messages.success(request, 'Membership deleted!')
    return redirect(reverse('membership_list'))
