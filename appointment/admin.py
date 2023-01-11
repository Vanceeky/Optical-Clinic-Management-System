from django.contrib import admin
from .models import *

# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone')
    ordering = ["-date_created"]
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'request_date', 'status', 'appointment_date', 'appointment_time')
    ordering = ["request_date"]
    def appointment_time(self, obj):
        return obj.strftime("%H:%M")
admin.site.register(Appointment, AppointmentAdmin)