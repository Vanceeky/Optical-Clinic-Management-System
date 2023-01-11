from django.db import models

# Create your models here.

class Patient(models.Model):

    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    firstname = models.CharField(max_length = 255, null = True)
    lastname = models.CharField(max_length = 255, null = True)  
    age = models.CharField(max_length = 255, null = True)  
    email = models.CharField(max_length = 255, null = True)

    gender = models.CharField(max_length=6, null = True, blank = True, choices = gender_choices)
    phone = models.CharField(max_length = 11, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Appointment(models.Model):
    Status = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )

    patient = models.ForeignKey(Patient, null = True, on_delete = models.CASCADE)

    message = models.TextField(max_length=255, null = True, blank = True)
    request_date = models.DateField(auto_now_add=False, null = True)

    sent_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length = 255, choices = Status, default = 'Pending')

    appointment_date = models.DateField(auto_now_add=False, null=True, blank = True)
    
    appointment_time = models.TimeField(auto_now_add = False, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f'{self.patient}' 