from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from.forms import UserEditForm,ProfileEditForm
from django.contrib.auth import views as auth_views
from doctor.models import Doctor
from.models	import Profile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.conf import settings
from patient.models import Patient
from django.contrib.auth.models import User,auth
import json,requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators	import	login_required

def doctor_autherization(user):
    try:
        return user.profile.role=='doctor'
    except ObjectDoesNotExist:
        pass
def patient_autherization(user):
    try:
        return user.profile.role=='patient'
    except ObjectDoesNotExist:
        pass
def receptionist_autherization(user):
    try:
        return user.profile.role=='receptionist'
    except ObjectDoesNotExist:
        pass
def hr_autherization(user):
    try:
        return user.profile.role=='hr'
    except ObjectDoesNotExist:
        pass

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if Profile.objects.filter(user=a).exists():
                b=Profile.objects.get(user=a.pk)
                if b.role=='doctor' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/doctor/doctordash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/login/')
                elif b.role=='patient' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/patient/patientdash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/login/')
                elif b.role=='hr' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/hr/hrdash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/login/')
                elif b.role=='receptionist' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/reception/receptiondash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/login/')
                
                else:
                    messages.info(request,'Your Account is not Activated by HR')  
                    return redirect('/account/login/')
            else:
                messages.info(request,'Unauthrized Access')
                return redirect('/account/login/')
        else:
            messages.info(request,'Your Account is not Created. Kindly Register Yourself')  
            return redirect('/account/login/')
    
    return render(request,"registration/login.html")

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

def	registration(request):
    if	request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        age=request.POST['age']
        role=request.POST['role']
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already exists")
                return redirect('/account/registration/')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
                return redirect('/account/registration/')
            else:
                new_user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                new_user.save()
                if role=='patient':
                    Profile.objects.create(user=new_user,role=role,activate=True)
                    Patient.objects.create(patient_id=new_user,age=age)	
                    return	render(request,'registration/patient_signup_done.html',{'new_user':new_user})
                    
                elif role=='doctor':
                    Doctor.objects.create(doctor_id=new_user,age=age)
                    Profile.objects.create(user=new_user,role=role,activate=True)	
                    return	render(request,'registration/registration_done.html',{'new_user':new_user})
        else:
            messages.info(request,"password didn't match ")
            return redirect('/registration/registration.html')
    
    return	render(request,	'registration/registration.html')



@login_required
@user_passes_test(doctor_autherization,login_url='/account/login/')  
def DoctorPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('doctor_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'registration/doctor_pass_change.html', {'form': form})
@login_required
@user_passes_test(patient_autherization,login_url='/account/login/')  
def PatientPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('patient_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'registration/patient_pass_change.html', {'form': form})
@login_required
@user_passes_test(receptionist_autherization,login_url='/account/login/')  
def ReceptionistPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('reception_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'registration/receptionist_pass_change.html', {'form': form})
@login_required
@user_passes_test(hr_autherization,login_url='/account/login/')  
def HrPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('hr_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'registration/hr_pass_change.html', {'form': form})

@login_required
@user_passes_test(doctor_autherization,login_url='/account/login/')
def	doctoredit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return  redirect('doctor_dash')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            return  redirect('doctor_dash')
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'registration/doctor_edit.html',{'user_form':user_form,'profile_form':profile_form})
@login_required
@user_passes_test(patient_autherization,login_url='/account/login/')
def	patientedit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return  redirect('patient_dash')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            return  redirect('patient_dash')
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'registration/patient_edit.html',{'user_form':user_form,'profile_form':profile_form})
@login_required
@user_passes_test(receptionist_autherization,login_url='/account/login/')
def	receptionistedit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return  redirect('reception_dash')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            return  redirect('reception_dash')
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'registration/receptionist_edit.html',{'user_form':user_form,'profile_form':profile_form})
@login_required
@user_passes_test(hr_autherization,login_url='/account/login/')
def	hredit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return  redirect('hr_dash')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            return  redirect('hr_dash')
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'registration/hr_edit.html',{'user_form':user_form,'profile_form':profile_form})


"""def doctor_autherization(user):
    try:
        return user.profile.designation=='hod'
    except ObjectDoesNotExist:
        pass
def admin_autherization(user):
    try:
        return user.adminprofile.role=='admin'
    except ObjectDoesNotExist:
        pass


def teacher_autherization(user):
    try:
        return user.profile.designation=='faculty'
    except ObjectDoesNotExist:
        pass
def user_autherization(user):
    try:
        return user.studentprofile.role=='student'
    except ObjectDoesNotExist:
        pass

def	teacher_login(request):
  
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if Profile.objects.filter(user=a).exists():
                b=Profile.objects.get(user=a.pk)
                if b.designation=='faculty' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/account/teacherdash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/teacherlogin/')
                else:
                    messages.info(request,'Your Account is not Activated by Admin')  
                    return redirect('/account/teacherlogin/')
            else:
                messages.info(request,'Unauthrized Access')
                return redirect('/account/teacherlogin/')
        else:
            messages.info(request,'Your Account is not Created. Kindly Register Yourself')  
            return redirect('/account/teacherlogin/')
    return	render(request,	'registration/teacher_login.html')

def	hod_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if Profile.objects.filter(user=a).exists():
                b=Profile.objects.get(user=a.pk)
                if b.designation=='hod' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/hod/hoddash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/hodlogin/')
                else:
                    messages.info(request,'Unauthrized Access')  
                    return redirect('/account/hodlogin/')
            else:
                messages.info(request,'Unauthrized Access')
                return redirect('/account/hodlogin/')
        else:
            messages.info(request,'You have not any  Account')  
            return redirect('/account/hodlogin/')
    return	render(request,	'account/hod_login.html')

def	admin_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if AdminProfile.objects.filter(user=a).exists():
                b=AdminProfile.objects.get(user=a.pk)
                if b.role=='admin' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/admins/admindash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/adminlogin/')
                else:
                    messages.info(request,'Unauthrized Access')  
                    return redirect('/account/adminlogin/')
            else:
                messages.info(request,'Unauthrized Access')
                return redirect('/account/adminlogin/')
        else:
            messages.info(request,'You have not any  Account')  
            return redirect('/account/adminlogin/')
    return	render(request,	'account/admin_login.html')


        
        
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')   
def teacher_dash(request):
    return	render(request,	'account/dashboard.html')
@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')    
def teacher_logout(request):
    auth.logout(request)
    return redirect('teacher_login')
@user_passes_test(admin_autherization,login_url='/account/adminlogin/')    
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')

def	student_login(request):
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            a=User.objects.get(username=username)
            if StudentProfile.objects.filter(user=a).exists():
                b=StudentProfile.objects.get(user=a.pk)
                if b.role=='student' and b.activate==True:
                    user=auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return	redirect('/user/studentdash/')
                    else:
                        messages.info(request,'Invalid Username or password')  
                        return redirect('/account/student_login/')
                else:
                    messages.info(request,'Your Account is not Activated by Tutour Guardian')  
                    return redirect('/account/student_login/')
            else:
                messages.info(request,'Unauthrized Access')
                return redirect('/account/student_login/')
        else:
            messages.info(request,'Your Account is not Created. Kindly Register Yourself')  
            return redirect('/account/student_login/')
 
    return render(request,'account/student_login.html')

@user_passes_test(user_autherization,login_url='/account/studentlogin/')
def student_logout(request):
    auth.logout(request)
    return redirect('student_login')

@user_passes_test(hod_autherization,login_url='/account/hodlogin/')  
def hod_logout(request):
    auth.logout(request)
    return redirect('hod_login')


def	register(request):
    if	request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        photo=request.FILES['photo']
        designation=request.POST['designation']
        department=request.POST['department']
        if designation=='hod':
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"username already exists")
                    return redirect('/account/register/')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"email already taken")
                    return redirect('/account/register/')
                else:
                    new_user=User.objects.create_superuser(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                    new_user.save()
                    Profile.objects.create(user=new_user,department=department,designation=designation,photo=photo)	
                    return	render(request,'account/register_done.html',{'new_user':	new_user})
            else:
                messages.info(request,"password didn't match ")
                return redirect('/account/register/')
        elif designation=='faculty':
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"username already exists")
                    return redirect('/account/register/')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"email already taken")
                    return redirect('/account/register/')
                else:
                    new_user=User.objects.create_superuser(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                    new_user.save()
                    Profile.objects.create(user=new_user,department=department,designation=designation,photo=photo,activate=False)	
                    return	render(request,'account/register_done.html',{'new_user':new_user})
            else:
                messages.info(request,"password didn't match ")
                return redirect('/account/register/')
        else:
            return	render(request,	'account/register.html')
    return	render(request,	'account/register.html')

def	StudentRegister(request):
    if	request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        photo=request.FILES['photo']
        role=request.POST['role']
        department=request.POST['department']
        batch=request.POST['batch']
        sec=request.POST['sec']
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already exists")
                return redirect('/account/studentregister/')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
                return redirect('/account/studentregister/')

            else:
                new_user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                
                new_user.save()
                StudentProfile.objects.create(user=new_user,department=department,role=role,batch=batch,photo=photo,sec=sec)	
                


                return	render(request,'account/register_done.html',{'new_user':	new_user})
        else:
            messages.info(request,"password didn't match ")
            return redirect('/account/studentregister/')
    else:
        return	render(request,	'account/studentregister.html')
    								
        			
    return	render(request,	'account/studentregister.html')

@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def	adminedit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=AdminProfileEditForm(instance=request.user.adminprofile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return  redirect('admin_dash')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            return  redirect('admin_dash')
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=AdminProfileEditForm(instance=request.user.adminprofile)				
    return	render(request,'account/adminedit.html',{'user_form':user_form,'profile_form':profile_form})



@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def	hodedit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return	redirect('hod_dash')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'account/hod_edit.html',{'user_form':user_form,'profile_form':profile_form})


@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def	edit(request):				
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return	render(request,'account/dashboard.html')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=ProfileEditForm(instance=request.user.profile)				
    return	render(request,'registration/edit.html',{'user_form':user_form,'profile_form':profile_form})

@user_passes_test(user_autherization,login_url='/account/studentlogin/')
def	student_edit(request):
    if request.method=='POST':								
        user_form=UserEditForm(instance=request.user,data=request.POST)								
        profile_form=StudentProfileEditForm(instance=request.user.studentprofile,data=request.POST,files=request.FILES)								
        if	user_form.is_valid()and	profile_form.is_valid():
            user_form.save()												
            profile_form.save()	
            messages.success(request,'Profile	updated	'\
                                        	'successfully')	
            return	render(request,'user/student_dash.html')
            
        else:												
            messages.error(request,'Error updating your	profile')		
            
    else:								
        user_form=UserEditForm(instance=request.user)								
        profile_form=StudentProfileEditForm(instance=request.user.studentprofile)				
    return	render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})
				
@user_passes_test(user_autherization,login_url='/account/studentlogin/')
def StudentPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your password was successfully updated!')
            return render(request,'user/student_dash.html')
        else:
            messages.error(request,'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/change_password.html', {'form': form})

@user_passes_test(teacher_autherization,login_url='/account/teacherlogin/')
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return	render(request,'account/dashboard.html')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'registration/password_change.html', {'form': form})


@user_passes_test(hod_autherization,login_url='/account/hodlogin/')
def HodPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('hod_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/hod_pass_change.html', {'form': form})

@user_passes_test(admin_autherization,login_url='/account/adminlogin/')
def AdminPasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_dash')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'account/admin_pass_change.html', {'form': form})"""




        