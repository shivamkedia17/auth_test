# forms.py

from django import forms

class FileForm(forms.Form):
    file_id = forms.CharField(label='Text Input', max_length=100, required=True)
