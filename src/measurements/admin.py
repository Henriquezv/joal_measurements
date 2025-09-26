from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MeasurementsGroup
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("name", "login", "email", "company_role", "is_admin", "is_active", "date_created")
    list_filter = ("company_role", "is_admin", "is_active")
    search_fields = ("name", "login", "email")
    ordering = ("date_created",)

    # Campos somente leitura
    readonly_fields = ("date_created", "last_login")

    fieldsets = (
        (None, {"fields": ("login", "password")}),
        ("Informações pessoais", {"fields": ("name", "email", "company_role", "company_id")}),
        ("Permissões", {"fields": ("is_active", "is_admin", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_created")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("login", "name", "email", "company_role", "password1", "password2", "groups"),
        }),
    )


@admin.register(MeasurementsGroup)
class MeasurementsGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
