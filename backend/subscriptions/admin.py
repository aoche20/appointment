from django.contrib import admin

from .models import Plan, Subscription  
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'online_payment')
    search_fields = ('name',)
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):      
    list_display = ('salon', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan__name')
    search_fields = ('salon__name', 'plan__name')

