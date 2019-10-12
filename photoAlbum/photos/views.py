from django.views.generic.edit import FormView, CreateView
from photos import forms, models, utils
# import photos.forms as forms  # FileFieldForm
from django.http import HttpResponse
from django.db import transaction


class AddAttributesView(FormView):
    form_class = forms.AddAttributesForm
    template_name = 'photos/add_attributes_view.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_id = self.kwargs['photo_id']
        photo = models.Photo.objects.get(id=photo_id)
        # TODO: WHy isn't it loadnig the image?
        context['photo_url'] = photo.document.url
        return context


class UploadPhotoView(CreateView):
    model = models.Photo
    template_name = 'photos/upload_photo_view.html'
    form_class = forms.UploadPhotoForm
    # success_url = reverse_lazy('images:upload')

    def form_valid(self, form):
        result_str = 'failed'
        with transaction.atomic():
            photo = form.save(commit=False)
            doc = photo.document
            #doc.save(name=doc.name, content=doc)
            photo.photo_hash = utils.hash_image(doc.path)
            # TODO: Make thumbnails of photos
            photo.save()
            result_str = 'success upload {}'.format(photo.photo_hash)
        return HttpResponse(result_str)


# TODO: Figure out how to  upload multiple images at a time
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
