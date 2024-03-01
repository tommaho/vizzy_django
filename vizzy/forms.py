from django import forms

from .models import DataSet

class DataSetForm(forms.Form):
    file_name = forms.CharField(max_length=100)
    file_upload = forms.FileField()

    def normalized(self):
        file_name = self.cleaned_data['file_name']

        return file_name