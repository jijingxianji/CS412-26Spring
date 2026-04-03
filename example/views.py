# file: example/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random


# Create your views here.
def home(request):
    ''' Function to respond to the home request '''
    response_text = f'''
    <html>
    <h1>"Hello, World!"</h1>
    the current time is {time.ctime()}.
    </html>
    '''
    return HttpResponse(response_text)

def home_page(request):
    ''' Response to the URL '', deleget work to a template '''
    template_name = 'example/home.html'

    # a dict of context variables (key-value paris)
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65, 90)),
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 10),
    }

    return render(request, template_name, context)


def about(request):
    ''' Response to the URL 'about', deleget work to a template '''
    template_name = 'example/about.html'

    # a dict of context variables (key-value paris)
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65, 90)),
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 10),
    }

    return render(request, template_name, context)
