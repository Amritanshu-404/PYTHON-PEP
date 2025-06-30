from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("This is the root Page.")

def loginpage(request):
    return render(request, 'index.html') 

