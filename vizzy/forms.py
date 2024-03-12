from django import forms

from .models import DataSet
from .validators import has_correct_mime_type
from .validators import has_csv_extension
from .validators import has_valid_encoding
from .validators import is_well_formed_csv

class DataSetForm(forms.Form):
    file_name = forms.CharField(max_length=100)
    file_upload = forms.FileField(validators=[
        has_csv_extension,
        has_valid_encoding,
        has_correct_mime_type,
        is_well_formed_csv,
    ])

    #     
    def normalized(self):
        file_name = self.cleaned_data['file_name']

        return file_name