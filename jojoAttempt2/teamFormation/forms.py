from django import forms
# from .models import upload, size, characteristics
from .models import csvUpload, teamSize, pickCols

class fileForm(forms.ModelForm):
    class Meta:
        model = csvUpload
        fields = '__all__'

class colForm(forms.ModelForm):
    COL_CHOICES =(
        ("1", "Similar"),
        ("2", "Different"),
        ("3", "Ignore"),
    )
    choice = forms.TypedChoiceField(choices = COL_CHOICES)
    class Meta:
        model = pickCols
        fields = '__all__'


class teamSizeForm(forms.ModelForm):
    class Meta:
        model = teamSize
        fields = '__all__'