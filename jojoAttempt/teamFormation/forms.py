from django import forms
#from .models import upload, size, characteristics

#Step 1
# class uploadForm(forms.ModelForm):
#     class Meta:
#         model = upload
#         fields = '__all__'
#
# #Step 2
# class sizeForm(forms.ModelForm):
#     class Meta:
#         model = size
#         fields = '__all__'
#
# #Step 3
# class characteristicsForm(forms.ModelForm):
#     class Meta:
#         model = characteristics
#         fields = '__all__'

### Malo Attempt: using Forms instead of ModelForm

class uploadForm(forms.Form): # PROBLEM: WHEN forms.FileField, a problem arises…
    uploaded_file = forms.IntegerField(help_text = 'Upload a .csv file.')

class sizeForm(forms.Form):
    team_size = forms.IntegerField(help_text = 'Enter the team size.')

class characteristicsForm(forms.Form):
    team_characteristics = forms.CharField(help_text = 'Enter the team characteristics.')
