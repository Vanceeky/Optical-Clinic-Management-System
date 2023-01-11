import django_filters

from appointment.models import *

class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = ['patient', 'status']

