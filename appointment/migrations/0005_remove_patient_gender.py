# Generated by Django 4.1.4 on 2023-01-10 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_remove_patient_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='gender',
        ),
    ]
