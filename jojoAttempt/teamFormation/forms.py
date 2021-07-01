from django import forms
from .models import upload, size, characteristics

#Step 1
class uploadForm(forms.ModelForm):
    class Meta:
        model = upload
        fields = '__all__'

#Step 2
class sizeForm(forms.ModelForm):
    class Meta:
        model = size
        fields = '__all__'

#Step 3
class characteristicsForm(forms.ModelForm):
    class Meta:
        model = characteristics
        fields = '__all__'