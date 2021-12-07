from django.shortcuts import render
from userprofiles.models import Userprofile

# from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect, JsonResponse
# from django.shortcuts import redirect, request


def index(request):
    return render(request, 'home/index.html')


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
    return render(request, 'home/register.html', context)


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
