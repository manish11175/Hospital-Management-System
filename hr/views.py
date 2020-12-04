from django.shortcuts import render,redirect
from account.models import Profile
from reception.models import Receptionist
from doctor.models import Doctor
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators	import	login_required
from patient.models import Patient,PatientPayment
def hr_autherization(user):
    try:
        return user.profile.role=='hr'
    except ObjectDoesNotExist:
        pass

@login_required
@user_passes_test(hr_autherization,login_url='/account/login/')
def hr_dash(request):
    return render(request,'hr/hr_dash.html')

@login_required
@user_passes_test(hr_autherization,login_url='/account/login/')
def create_user(request):
    if	request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        gender=request.POST['gender']
        role=request.POST['role']
        age=request.POST['age']
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already exists")
                return redirect('/hr/create_user/')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
                return redirect('/hr/create_user/')
            else:
                new_user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                new_user.save()
                if role=='receptionist':
                    r=Receptionist.objects.create(receptionist_id=new_user,gender=gender,age=age)
                    
                    p=Profile.objects.create(user=new_user,role=role,activate=True)	
                 
                    return	render(request,'hr/create_user_done.html',{'new_user':new_user})
                    
                elif role=='hr':
                    Profile.objects.create(user=new_user,role=role,activate=True)	
                    return	render(request,'hr/create_user_done.html',{'new_user':new_user})
        else:
            messages.info(request,"password didn't match ")
            return redirect('/hr/create_user/')
    return render(request,'hr/create_user.html')
        
@login_required
@user_passes_test(hr_autherization,login_url='/account/login/')
def doctors(request):

    a_doc=Doctor.objects.filter(active=True)
    d_doc=Doctor.objects.filter(active=False)
    return render(request,'hr/doctors.html',{'a_doc':a_doc,'d_doc':d_doc})
