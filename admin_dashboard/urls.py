from django.urls import path
from .views import Manage_Appointment
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard'),
    path('dashboard/manage_appointment/add', views.add_appointment, name='add_appointment'),
    path('dashboard/patient_list/', views.patient_list, name='patient_list'),
    path('dashboard/patient_list/<str:pk>/', views.view_appointment, name='patient'),
    path('dashboard/manage_appointments/', Manage_Appointment.as_view(), name='manage_appointments'),
    path('dashboard/manage_appointment/cancelled/<str:pk>/', views.cancel_request, name='cancel_request'),
    path('dashboard/patient_list/rescheduled/<str:pk>/', views.reschedule, name='reschedule'),
    path('dashboard/patient_list/completed/<str:pk>/', views.completed, name='completed'),
    path('dashboard/delete_appointment/<str:pk>/', views.delete_appointment, name='delete_appointment'),
]
