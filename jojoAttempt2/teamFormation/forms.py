from django import forms
# from .models import upload, size, characteristics
from .models import csvUpload, teamSize, pickCols

class fileForm(forms.ModelForm):
    class Meta:
        model = csvUpload
        fields = ('csvFile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csvFile'].widget.attrs.update({'class': 'form-control'})
        self.fields['csvFile'].label = "Enter your CSV or Excel file"


class colForm(forms.ModelForm):
    # We need to create an __init__ method to dynamically create fields
    def __init__(self, columns, *args, **kwargs): # columns argument represent the name of the form’s fields
        COL_CHOICES =(
            ("1", "Similar"),
            ("2", "Different"),
            ("3", "Ignore"),
        )

        super().__init__(*args, **kwargs)
        column_list = columns
        for i in range(len(column_list)):
            field_name = column_list[i]
            self.fields[field_name] = forms.TypedChoiceField(choices = COL_CHOICES, required=True)
            self.fields[field_name].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = pickCols
        fields = '__all__'


class teamSizeForm(forms.ModelForm):
    class Meta:
        model = teamSize
        fields = ('size',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].widget.attrs.update({'class': 'form-control'})
        self.fields['size'].label = 'Team Size'
