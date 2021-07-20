from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse


'''
Level Constant	Tag	    Value
DEBUG	        debug	10
INFO	        info	20
SUCCESS	        success	25
WARNING	        warning	30
ERROR	        error	40
'''

def MessageBasicView(request):
    
    # there are two ways to add a message in view code
    # (a) using the add_message method, 
    messages.add_message(request, messages.INFO, 'Hello!')

    # (b) using one of the convenience methods for the message level (info in this case).
    messages.info(request, 'Hello!')
    return render(request,'basic_skills/messages/message_test.html')


def MessageNoTemplateView(request):    
    messages.debug (request, 'Hello! debug')
    messages.info (request, 'Hello! info')
    messages.success (request, 'Hello! success')
    messages.warning (request, 'Hello! warning')
    messages.error (request, 'Hello! error')
    return HttpResponse()