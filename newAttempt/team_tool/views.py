from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from team_tool.forms import SurveyInput
from django.core.files.storage import FileSystemStorage


# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

def survey_input(request):
    if request.method == 'POST':
        survey_data = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(survey_data.name, survey_data)
        context = {'file_name': survey_data.name, 'file_size': survey_data.size, 'file': survey_data}
        return render(request, 'survey_step_2.html', context = context)
    return render(request, 'survey_input.html')
