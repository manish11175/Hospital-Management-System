from django.db import models


from django.db import models 
from django.conf import settings
role	=	(('doctor','doctor'),('patient','patient'),('hr','hr'),('receptionist','receptionist'))
Activate=(('activate','activate'),('deactivate','deactivate'))

class Profile(models.Model):				
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role=models.CharField(max_length=30,default="admin",choices=role)	
    date_of_birth=models.DateField(blank=True,	null=True)
    contact_no=models.CharField(max_length=10,blank=False,default="")
    photo=models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    activate=models.BooleanField(default=False)
    join_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
