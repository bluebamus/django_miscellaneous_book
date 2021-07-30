from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    
    return HttpResponse('<html><title>일정관리</title></html>') # success
    #return HttpResponse('<html></html>') 