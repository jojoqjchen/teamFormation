from django import forms
from . import validators

class SurveyInput(forms.Form):
    csvFile = forms.FileField(help_text = "Please enter a csv file", validators = [validators.validate_file_extension])
