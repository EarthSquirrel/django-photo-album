from django.views.generic.edit import FormView
import photos.forms as forms  # FileFieldForm


class AddAttributesView(FormView):
    form_class = forms.AddAttributesForm
    template_name = 'images/add_attribute_view.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: Get the image to project
        context['img_url'] = 'url to image'
        return context


class FileFieldView(FormView):
    form_class = forms.FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                pass  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
