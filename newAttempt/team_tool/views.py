from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from team_tool.forms import SurveyInput
from django.core.files.storage import FileSystemStorage
import pandas as pd
import csv, io
from django.contrib.auth.decorators import login_required

from .forms import SurveyInput

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

@login_required
def survey_input(request):
    if request.method == 'POST':
        form = SurveyInput(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'survey_step_2.html')
    else:
        form = SurveyInput()
    return render(request, 'upload_form.html', {
        'form': form,
    })
