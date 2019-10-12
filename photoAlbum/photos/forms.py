from django import forms


class AddAttributesForm(forms.Form):
    dummy_attribute = forms.CharField()


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(
                                 attrs={'multiple': True}))
