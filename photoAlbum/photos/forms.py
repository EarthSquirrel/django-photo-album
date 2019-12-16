from django import forms
from photos import models
from dal import autocomplete as ac


class UploadPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ['document']


class AddAttributesForm(forms.Form):
    # dummy_attribute = forms.CharField()
    people = forms.ModelMultipleChoiceField(queryset=models.Person.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/person-ac/'))



class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(
                                 attrs={'multiple': True}))
