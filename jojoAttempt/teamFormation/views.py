from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.views.generic import TemplateView
# from django.core.files.storage import FileSystemStorage
# from django.shortcuts import redirect
# from django.urls import reverse 
# from django.views.generic import FormView
# from . import constants

from .models import upload, size, characteristics
from .forms import uploadForm, sizeForm, characteristicsForm
import os

# Create your views here.

def home(request):
    return render(request, 'home.html')

class multiFormSubmission(SessionWizardView):
    template_name = 'form.html'
    form_list = [uploadForm, sizeForm, characteristicsForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'csv'))

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        return render(self.request, 'home.html', {
            'data' : form_data
        })
# def getCurrForm(session_hash):
#     # Returns an incomplete form response with a matching session hashcode or None
#     # if the object does not exist 
#     return teams.objects.filter(
#         session_hash=session_hash, 
#     ).exclude(
#         stage = constants.COMPLETE
#     ).first()

# class teamsFormView(FormView):
#     template = 'home.html'
#     form = None
#     form_class = None 

# #get the form for this session
# def dispatch(self, request, *args, **kwargs):
#     session_hash = request.session.get("session_hash", None)
    
#     #get the form for the current session 
#     self.form = getCurrForm(session_hash)
#     #attach the request to "self" to be accessed later 


# def home(request):
#     context = {}
#     if request.method == 'POST':
#         form = teamsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('uploaded')

#     else:
#         form = teamsForm()

#     context['form'] = teamsForm()
#     return render(request, 'home.html', {
#         'form': form
#     })