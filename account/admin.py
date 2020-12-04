from django.contrib import admin
from.models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):				
    list_display=['user','photo','contact_no','role','activate']
    list_filter	=('user','role','activate')
   
    
    class Meta:
        ordering = ['-user']
