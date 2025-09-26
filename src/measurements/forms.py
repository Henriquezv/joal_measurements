from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import User, MeasurementsGroup


class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=MeasurementsGroup.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        label="Grupos",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("login", "name", "email", "company_role", "password1", "password2", "groups")


class CustomUserChangeForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=MeasurementsGroup.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        label="Grupos",
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("login", "name", "email", "company_role", "is_active", "is_admin", "groups")


# Alias para compatibilidade com views antigas
CreateUserForm = CustomUserCreationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite seu login"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"}),
    )
