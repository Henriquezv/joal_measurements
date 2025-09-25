from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, CustomAuthenticationForm
from .decorators import unauthenticated_user


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')
    else:
        form = CreateUserForm()

    return render(request, 'measurements/register.html', {'form': form})


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login_field = form.cleaned_data.get('username')  # username agora é login
            password = form.cleaned_data.get('password')
            user = authenticate(username=login_field, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.name}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'measurements/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


@login_required
def home(request):
    return render(request, 'measurements/home.html')


@login_required
def manager(request):
    return render(request, 'measurements/manager.html')


@login_required
def engineer(request):
    return render(request, 'measurements/engineer.html')


@login_required
def dashboard(request):
    return render(request, 'measurements/dashboard.html')


@login_required
def board(request):
    return render(request, 'measurements/board.html')