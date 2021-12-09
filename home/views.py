from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'home/index.html')


def login(request):
    return render(request, 'home/login.html')


def logout(request):
    return render(request, 'home/logout.html')
