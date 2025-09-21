from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'measurements/home.html')

def manager(request):
    return render(request, 'measurements/manager.html')

def engineer(request):
    return render(request, 'measurements/engineer.html')

def dashboard(request):
    return render(request, 'measurements/dashboard.html')

def board(request):
    return render(request, 'measurements/board.html')


