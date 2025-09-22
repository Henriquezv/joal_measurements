from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'login', 'company_role', 'is_admin', 'date_created')
    search_fields = ('name', 'login')
    list_filter = ('company_role', 'is_admin')
    ordering = ('-date_created',)
