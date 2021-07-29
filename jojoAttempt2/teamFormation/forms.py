from django import forms
# from .models import upload, size, characteristics
from .models import csvUpload, teamSize, pickCols, projectFirstParam

class fileForm(forms.ModelForm):
    class Meta:
        model = csvUpload
        fields = ('csvFile','algorithm')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csvFile'].widget.attrs.update({'class': 'form-control'})
        self.fields['csvFile'].label = "Enter your CSV or Excel file"
        self.fields['algorithm'].widget.attrs.update({'class': 'form-select'})


class colForm(forms.ModelForm):
    # We need to create an __init__ method to dynamically create fields
    def __init__(self, columns, colNameIsNumeric, *args, **kwargs): # columns argument represent the name of the form’s fields
        COL_CHOICES =(
            ("1", "Similar"),
            ("2", "Different"),
            ("3", "Ignore"),
        )

        super().__init__(*args, **kwargs)
        column_list = columns
        for i in range(len(column_list)): # IF TWO COLUMNS HAVE THE SAME NAME, UNWANTED BEHAVIOR HAPPENS
            if column_list[i] in colNameIsNumeric:
                default = "1"
                field_name = column_list[i]
                self.fields[field_name] = forms.TypedChoiceField(choices = COL_CHOICES, required=True, initial = default)
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

class projectFirstParamForm(forms.ModelForm):
    class Meta:
        model = projectFirstParam
        fields = ('numberOfProjects','numberOfChoices')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numberOfProjects'].widget.attrs.update({'class': 'form-control'})
        self.fields['numberOfProjects'].label = 'Number of different Projects'
        self.fields['numberOfChoices'].widget.attrs.update({'class': 'form-control'})
        self.fields['numberOfChoices'].label = 'Number of choices per individual'
