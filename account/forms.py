from django import forms
from.models import Profile
from django.contrib.auth.models	import	User
class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'input'}))				
    password2=forms.CharField(label='Repeat	password',widget=forms.PasswordInput(attrs={'class':'input'}))

    class Meta:

        model=User								
        fields=('username','first_name','last_name','email')
        
    def	clean_password2(self):							
        cd=self.cleaned_data								
        if	cd['password']!=cd['password2']:												
            raise	forms.ValidationError('Passwords	don\'t	match.')								
        return	cd['password2']
class UserEditForm(forms.ModelForm):				
    class Meta:								
        model=User
        fields=('first_name','last_name','email')
        widgets={
                'email':forms.EmailInput(attrs={'class':'input'}),
                'first_name':forms.TextInput(attrs={'class':'input'}),
                'last_name':forms.TextInput(attrs={'class':'input'}),}
class ProfileEditForm(forms.ModelForm):				
    class Meta:								
        model	=Profile								
        fields	=	('date_of_birth','photo','contact_no')
        widgets={
                'date_of_birth':forms.DateInput(attrs={'class':'input'}),
                'photo':forms.FileInput(attrs={'class':'input'}),
                'contact_no':forms.NumberInput(attrs={'class':'input'})}
