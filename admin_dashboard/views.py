from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import datetime

from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.template.loader import get_template
from django.core.mail import EmailMessage, message
from django.contrib import messages

from appointment.models import *
from inventory.models import *

from django.contrib.auth.models import User

from .filter import PatientFilter

from authentication.decorators import *
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

def page_not_found_view(request, exception):
    return render(request, 'layouts/404.html', status=404)

@login_required(login_url="login")
@admin_only
def index(request):

    appointments = Appointment.objects.all()
    patients = Patient.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()


    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    today = datetime.datetime.now()

    todays_appointment = Appointment.objects.filter(appointment_date__year = year, appointment_date__month= month, appointment_date__day = day)

    upcoming_appointment = Appointment.objects.filter(appointment_date__gt = today).order_by("-appointment_date")

    pending = appointments.filter(status = 'Pending')
    accepted = appointments.filter(status = 'Accepted')
    cancelled = appointments.filter(status = 'Cancelled')
    completed = appointments.filter(status = 'Completed')

    total_appointments = appointments.count()
    todays_count = appointments.filter(appointment_date = today).count()
    pending_count = appointments.filter(status = 'Pending').count()
    accepted_count = appointments.filter(status = 'Accepted').count()
    cancelled_count = appointments.filter(status = 'Cancelled').count()
    completed_count = appointments.filter(status = 'Completed').count()

    category_count = category.count()
    product_count = product.count()

    context = {

       # 'myFilter': myFilter,
        'appointment': appointments,
        'patient': patients,

        'todays_date':today,

        'todays_appointment': todays_appointment,
        'upcoming_appointment': upcoming_appointment,

        'pending': pending,
        'accepted': accepted,
        'cancelled': cancelled,
        'completed': completed,

        'total_appointments': total_appointments,
        'todays_count': todays_count,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,

        
        'category': category,
        'product': product,
        'category_count': category_count,
        'product_count': product_count,
    }

    return render(request, 'admin_dashboard/index.html', context)

#decorators = [never_cache, login_required]

class Manage_Appointment(ListView):


    appointment = Appointment.objects.all()

    template_name = 'admin_dashboard/manage_appointment.html'
    model = Appointment
    context_object_name = 'appointments'

    @method_decorator(login_required)
    def post(self, request):

        appointment_id = request.POST.get('appointment-id')
        appointment_time = request.POST.get('time')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = 'Accepted'
        appointment.appointment_date = appointment.request_date
        appointment.appointment_time = appointment_time
        appointment.save()
        

       # aw = appointment_id.count()

        data = {
            "fname": appointment.patient.firstname,
            "lname": appointment.patient.lastname,
            "date": appointment.request_date,
            "time": appointment.appointment_time
           # "time": time,
            
        }

        message = get_template('admin_dashboard/email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.patient.email],
        )

        email.content_subtype = "html"
        email.send()

        messages.success(request, ' Email has been sent! ')
        

        return redirect('manage_appointments')   
        

def add_appointment(request):

        appointment = Appointment.objects.all()
        patient = Patient.objects.all()



        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        age = request.POST.get('age')
        phone = request.POST.get('phone_number')

        appointment_date = request.POST.get('date')




        patient = Patient.objects.create(
                firstname = firstname,
                lastname = lastname,
                age = age,
                phone = phone,
        )

        patient.save()

        appointment = Appointment.objects.create(
                patient = patient,
                appointment_date = appointment_date,
                appointment_time = datetime.datetime.now(),
                status = 'Accepted'

        )

        appointment.save()
        
        messages.success(request, ' Appointment is Saved! ')

        return redirect('dashboard')


def completed(request, pk):
    appointment = Appointment.objects.get(id = pk)

    if request.method == "POST":
        appointment.status = 'Completed'
        appointment.save()

    context = {
        'appointment': appointment
    }

    return render(request, 'admin_dashboard/appointment_profile.html', context)    

   

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
@admin_only
def reschedule(request, pk):
    appointment = Appointment.objects.get(id =pk)
    if request.method == "POST":
        appointment_date = request.POST.get('date')
        appointment.appointment_date = appointment_date
        appointment.save()

        data = {
            "fname": appointment.patient.firstname,
            "lname": appointment.patient.lastname,
            "date": appointment.appointment_date,
            "time": appointment.appointment_time
           # "time": time,
            
        }

        message = get_template('admin_dashboard/reschedule_email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.patient.email],
        )

        email.content_subtype = "html"
        email.send()

        return redirect('manage_appointments')


    context = {
        'appointment': appointment
    }

    messages.success(request, ' Appointment is rescheduled! ')

    return render(request, 'admin_dashboard/appointment_profile.html', context)    


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
@admin_only
def cancel_request(request, pk):

    appointment = Appointment.objects.get(id=pk)
    if request.method == "POST":
        appointment.status = 'Cancelled'
        appointment.save()

        data = {
            "fname": appointment.patient.firstname,
            "lname": appointment.patient.lastname,
            "date": appointment.request_date,
            "time": appointment.appointment_time
           # "time": time,
            
        }

        message = get_template('admin_dashboard/cancel_email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.patient.email],
        )

        email.content_subtype = "html"
        email.send()

        return redirect('manage_appointments')

    context = {
        'appointment': appointment
    }
    return render(request, 'admin_dashboard/cancel.html', context)    

def delete_appointment(request, pk):
    appointment = Appointment.objects.get(id = pk)

    appointment.delete()
    messages.success(request, ' Appointment successfully deleted!')
    return redirect('dashboard')


@allowed_users(allowed_roles=['admin'])
@admin_only
def patient_list(request):

    appointments = Appointment.objects.all()

    accepted_appointment = Appointment.objects.filter(status = 'Accepted')


    context = {
        'appointments': appointments,
        'accepted_appointment': accepted_appointment,
       # 'myFilter': myFilter
    }
    return render(request, 'admin_dashboard/patient_list.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
@admin_only
def view_appointment(request, pk):

    appointment = Appointment.objects.get(id = pk)

    context = {
        'appointment': appointment
    }

    return render(request, 'admin_dashboard/appointment_profile.html', context)