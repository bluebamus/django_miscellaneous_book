from django.http import HttpResponse
from django.shortcuts import render

# reference : https://wikidocs.net/11059

# Create your views here.
def home_page(request):
    
    #return HttpResponse('<html><title>일정관리</title></html>') # success
    #return HttpResponse('<html></html>') 
    return render(request, 'testcase_skills/home.html')


def home_page_post(request):
    return render(request, 'testcase_skills/home_post.html')