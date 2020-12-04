from.import views
from django.contrib.auth import views as auth_views
from django.urls import path,include

urlpatterns = [
            
            path('login/',views.login,name="login"),
            path('logout/',views.logout,name="logout"),
            path('registration/',views.registration,name="register"),
            
            path('doctor_password_change/',views.DoctorPasswordChange,name='doctor_password_change'), 
            path('patient_password_change/',views.PatientPasswordChange,name='patient_password_change'), 
            path('receptionist_password_change/',views.ReceptionistPasswordChange,name='receptionist_password_change'), 
            path('hr_password_change/',views.HrPasswordChange,name='hr_password_change'), 
            path('doctor_edit',views.doctoredit,name="doctor_edit"),
            path('patient_edit',views.patientedit,name="patient_edit"),
            path('receptionist_edit',views.receptionistedit,name="receptionist_edit"),
            path('hr_edit',views.hredit,name="hr_edit"),
            #path('password_reset/',	auth_views.PasswordResetView.as_view(),name='password_reset'),
            #path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
            #path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
            #path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
            
           
]

