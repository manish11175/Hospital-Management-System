
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import	static
from django.conf import	settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctor/',include('doctor.urls')),
    path('account/',include('account.urls')),

    path('hr/',include('hr.urls')),
  
    path('',include('home.urls')),
]
if	settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
