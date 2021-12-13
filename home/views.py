from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def login(request):
    return render(request, 'home/login.html')


def logout(request):
    return render(request, 'home/logout.html')


def forgot_password(request):
    return render(request, 'home/forgot_password.html')
