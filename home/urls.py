
from.import views
from django.urls import path,include

urlpatterns = [
                path('',views.index,name="home"),
                path('contact/',views.contact,name="contact"),
                path('services/',views.services,name="services")
]
