
from.import views
from django.urls import path,include

urlpatterns = [
                path('doctordash/',views.doctor_dash,name="doctor_dash"),
                path('doctor_appointment/',views.doctor_appointment,name="doctor_appointment"),
                path('doctor_prescription/',views.doctor_prescription,name="doctor_prescription"),
                path('prescriptions/',views.prescriptions,name="prescriptions"),
]
