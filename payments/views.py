from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'payments/index.html')


def register(request):
    return render(request, 'payments/register.html')


def home(request, username):
    return render(request, 'payments/home.html', {'username': username})


def statistics(request, username):
    return render(request, 'payments/statistics.html', {'username': username})


def settings(request, username):
    return render(request, 'payments/settings.html', {'username': username})


def search(request):
    return render(request, 'payments/search.html')
