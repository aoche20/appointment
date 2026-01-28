from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'price', 'duration', 'is_active')
    list_filter = ('salon', 'is_active')
    search_fields = ('name', 'salon__name')
    ordering = ('salon', 'name')
    readonly_fields = ('created_at',)
    