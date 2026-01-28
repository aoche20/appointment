from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'is_active')
    list_filter = ('salon', 'is_active')
    search_fields = ('name', 'salon__name')
    ordering = ('salon', 'name')