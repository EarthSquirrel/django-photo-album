from django import forms
from photos import models
from dal import autocomplete as ac


class UploadPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ['document', 'owner', 'device']
        widgets = {
            'owner':
            ac.ModelSelect2(url='/photos/person-ac/'),
            'device':
            ac.ModelSelect2(url='/photos/device-ac/')
        }

class AddAttributesForm(forms.Form):
    # dummy_attribute = forms.CharField()
    people = forms.ModelMultipleChoiceField(queryset=models.Person.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/person-ac/'))

    animals = forms.ModelMultipleChoiceField(queryset=models.Animal.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/animal-ac/'))

    location = forms.ModelMultipleChoiceField(queryset=models.Location.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/location-ac/'))

    events = forms.ModelMultipleChoiceField(queryset=models.Event.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/event-ac/'))



class SearchForm(forms.Form):
    owner = forms.ModelMultipleChoiceField(queryset=models.Person.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/person-ac/'))

    events = forms.ModelMultipleChoiceField(queryset=models.Event.objects.all(),
        required=False, widget=ac.ModelSelect2Multiple(url='/photos/event-ac/'))


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(
                                 attrs={'multiple': True}))
