from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('salon','service', 'employee','date', 'status','start_time', 'end_time')
    list_filter = ('salon', 'status', 'date')
 