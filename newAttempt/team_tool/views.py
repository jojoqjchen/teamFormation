from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from team_tool.forms import SurveyInput
from django.core.files.storage import FileSystemStorage
import pandas as pd
import csv, io

from .forms import SurveyInput

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'


def survey_input(request):
    if request.method == 'POST':
        form = SurveyInput(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            csv_file = request.FILES['csvFile']
            data_set = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            for line in lines:
                fields = line.split(",")
                print(fields[0])
            context = {'file_name': lines, 'file_size': 0, 'file': 0}
            return render(request, 'survey_step_2.html', context = context)
    else:
        form = SurveyInput()
    return render(request, 'upload_form.html', {
        'form': form,
    })
