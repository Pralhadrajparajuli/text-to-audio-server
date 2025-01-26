from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']

admin.site.register(CustomUser, CustomUserAdmin)