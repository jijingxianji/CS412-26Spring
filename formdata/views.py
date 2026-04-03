
# formdata/views.py
# view functions to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_form(request):
    '''Show the form to the user.'''

    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''Handle the form submission, and generate a result.'''

    print(request)
    return HttpResponse("")