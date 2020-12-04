from.import views
from django.urls import path,include

urlpatterns = [
            path('hrdash/',views.hr_dash,name="hr_dash"),
            path('create_user/',views.create_user,name="create_user"),
            path('doctors/',views.doctors,name="doctors"),
            path('<pk>/doctor_update/',views.doctor_update,name="doctor_update"),
            path('payment_details',views.patient_payment,name="payment_details"),
]


