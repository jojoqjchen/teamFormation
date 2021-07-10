from django import forms
from django import forms
from .models import Upload

class SurveyInput(forms.ModelForm):
    class Meta:
        model = Upload
        fields = '__all__'
