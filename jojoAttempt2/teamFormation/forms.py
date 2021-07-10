from django import forms
# from .models import upload, size, characteristics
from .models import csvUpload, pickCols

class fileForm(forms.ModelForm):
    class Meta:
        model = csvUpload
        fields = '__all__'

class colForm(forms.ModelForm):
    class Meta:
        model = pickCols
        fields = '__all__'

