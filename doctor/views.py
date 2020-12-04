from django.shortcuts import render,redirect
from django.http import HttpResponse
from reception.models import Appointment,PatientAppointment
from django.contrib import messages
from patient.models import Patient
from.models import Doctor,Prescription
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators	import	login_required
def doctor_autherization(user):
    try:
        return user.profile.role=='doctor'
    except ObjectDoesNotExist:
        pass

@login_required
@user_passes_test(doctor_autherization,login_url='/account/login/')
def doctor_dash(request):
    return render(request,'doctor/doctor_dash.html')
@login_required
@user_passes_test(doctor_autherization,login_url='/account/login/')
def doctor_appointment(request):
    a=[]
    b=[]
    if Appointment.objects.filter(docter=request.user.doctor).exists():
        a=Appointment.objects.filter(docter=request.user.doctor)
    if PatientAppointment.objects.filter(docter=request.user.doctor).exists():
        b=PatientAppointment.objects.filter(docter=request.user.doctor)
    else:
        messages.info(request,'You dont have appointment')
    return render(request,'doctor/doctor_appointment.html',{'a':a,'b':b})

@login_required
@user_passes_test(doctor_autherization,login_url='/account/login/')
def doctor_prescription(request):
    doctor=request.user.doctor
    patient=Patient.objects.all()
    if request.method=='POST':
        patient=request.POST['patient']
        date=request.POST['date']
        symptom=request.POST['symptom']
        prescription=request.POST['prescription']
        u=User.objects.get(username=patient)
        p=Patient.objects.get(patient_id=u)
        pre=Prescription.objects.create(doctor=doctor,patient=p,date=date,symptom=symptom,prescription=prescription)
        pre.save()
        messages.success(request,'Appointment Update Successfully')
        return redirect('doctor_dash')
    return render(request,'doctor/doctor_prescription.html',{'doctor':doctor,'patient':patient})
@login_required
@user_passes_test(doctor_autherization,login_url='/account/login/')
def prescriptions(request):
    prescription=Prescription.objects.all()
    return render(request,'doctor/prescriptions.html',{'prescription':prescription})
     