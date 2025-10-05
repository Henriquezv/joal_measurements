from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import User, MeasurementsGroup, Measurement


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


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = [
            "name",
            "contract",
            "start_date",
            "value",
            "discounts",
            "discounts_detail",
            "final_value",
            "description",
            "attachment",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contract": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "discounts": forms.NumberInput(attrs={"class": "form-control"}),
            "discounts_detail": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "final_value": forms.NumberInput(attrs={"class": "form-control"}),
            "description": CKEditor5Widget(config_name="default"),
        }