from django.contrib import admin
from .models import Salon

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'owner', 'is_active')
    list_filter = ('city', 'is_active')
