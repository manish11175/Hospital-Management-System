from django.contrib import admin
from.models import Doctor,Prescription
@admin.register(Doctor)
class DocterAdmin(admin.ModelAdmin):				
    list_display=['doctor_id','gender','age','specialist']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):				
    list_display=['doctor','patient','date','symptom','prescription']
    