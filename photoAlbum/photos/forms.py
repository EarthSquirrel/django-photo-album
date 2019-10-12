from django import forms
from photos import models


class UploadPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ['document']


class AddAttributesForm(forms.Form):
    dummy_attribute = forms.CharField()


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(
                                 attrs={'multiple': True}))
