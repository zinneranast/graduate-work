from django.shortcuts import render
from django.contrib import auth

def index(request):
    return render(request, 'index.html') #, {'username=': auth.get_user(request).username})
