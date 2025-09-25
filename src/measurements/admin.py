from django.contrib import admin
from .models import User, CompanyRole


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "login", "email", "company_role", "is_admin", "is_active", "date_created")
    list_filter = ("company_role", "is_admin", "is_active")
    search_fields = ("name", "login", "email")
    ordering = ("date_created",)