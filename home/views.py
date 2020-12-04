from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login

from django.contrib import messages

def index(request):
    return render(request,'home.html')
def contact(request):
    return render(request,'contact.html')
def services(request):
    return render(request,'services.html')
# Create your views here.
