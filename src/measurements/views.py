from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.forms import inlineformset_factory
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required



from .models import *

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'measurements/register.html', context)

from django.contrib.auth.hashers import check_password
from .models import User  # agora usa seu User e não o do Django

def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password_input = request.POST.get('password')

        try:
            user = User.objects.get(login=login_input)
            if check_password(password_input, user.password):
                # Autenticado com sucesso
                request.session['user_id'] = user.id  # salva na sessão
                messages.success(request, f'Bem-vindo, {user.name}!')
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')

    return render(request, 'measurements/login.html')  

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')      

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


