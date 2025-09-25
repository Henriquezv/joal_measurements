from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Formulário de criação de usuário
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['login', 'name', 'email', 'company_role', 'password1', 'password2']

# Formulário de login customizado
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Login")