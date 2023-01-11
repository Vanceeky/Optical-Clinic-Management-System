from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from datetime import datetime
from django.contrib import messages





# Create your views here.


    
class index(TemplateView):
    template_name = 'appointment/index.html'

    def post(self, request):
        
        appointment = Appointment.objects.all()
        patient = Patient.objects.all()



        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('radio')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')

        request_date = request.POST.get('date')
        message = request.POST.get('message')

        fname = patient.filter(firstname = firstname)
        lname = patient.filter(lastname = lastname)

        if(fname and lname).exists():
            messages.error(request, " You already sent a request, please check your email for updates! ")
            return redirect('/')

        else:


            patient = Patient.objects.create(
                            firstname = firstname,
                            lastname = lastname,
                            age = age,
                            email = email,
                            phone = phone,

            )

            patient.save()

            appointment = Appointment.objects.create(
                            patient = patient,
                            request_date = request_date,
                            message = message
            )

            appointment.save()

                



            messages.success(request, ' Your request is sent! We will send you update on your email within 24 hrs')

            return redirect('/')