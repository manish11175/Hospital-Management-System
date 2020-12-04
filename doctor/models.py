from patient.models import Patient

from django.db import models
from django.conf import settings
Gender=(('male','male'),('female','female'),('other','other'))

class Doctor(models.Model):				
    doctor_id=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    doctor_name=models.CharField(max_length=50,default="")
    specialist=models.CharField(max_length=30,default="")
    gender=models.CharField(max_length=10,choices=Gender,default="male")
    age=models.IntegerField(blank=True)
    address=models.CharField(max_length=100,default="")
    blood_group=models.CharField(max_length=30,default="")
    active=models.BooleanField(default=True)
class Prescription(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    date=models.DateField()
    symptom=models.CharField(max_length=200,default="")
    prescription=models.CharField(max_length=300,default="")