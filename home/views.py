from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def forgot_password(request):
    return render(request, 'home/forgot_password.html')
