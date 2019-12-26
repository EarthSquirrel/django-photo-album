from django.views.generic.edit import FormView, CreateView
from django.utils.datastructures import MultiValueDictKeyError
# “from django.views.generic.list import ListView
import django.views.generic as genViews
from photos import forms, models, utils
# import photos.forms as forms  # FileFieldForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from dal import autocomplete as ac


class AddAttributesView(FormView):
    form_class = forms.AddAttributesForm
    template_name = 'photos/add_attributes_view.html'

    
    def form_valid(self, form):
        photo_id = self.kwargs['photo_id']
        photo = models.Photo.objects.get(id=photo_id)
        data = form.cleaned_data
        events = data['events']
        if len(events) > 0:
            for i in events:
                models.EventTag.objects.get_or_create(photo=photo,
                                                      atr=i)
        
        # import pdb; pdb.set_trace()
        return HttpResponseRedirect(reverse('photos:photo_details', 
                                            args=[photo_id])) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_id = self.kwargs['photo_id']
        photo = models.Photo.objects.get(id=photo_id)
        context['photo_url'] = photo.large_thumb.url
        return context


class PhotoDetailsView(genViews.DetailView):
    model = models.Photo
    template_name = 'photos/photo_details_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = context['object']
        context['attributes'] = utils.get_html_attributes(photo)
        # import pdb; pdb.set_trace()
        return context


class UploadPhotoView(CreateView):
    model = models.Photo
    template_name = 'photos/upload_photo_view.html'
    form_class = forms.UploadPhotoForm

    def form_valid(self, form):
        result_str = 'failed'
        with transaction.atomic():
            photo = form.save(commit=False)
            doc = photo.document
            # Save document to get hash
            doc.save(name=doc.name, content=doc)
            photo.photo_hash = utils.hash_image(doc.path)
            # Create thumbnails of photots
            photo.small_thumb.save(name=doc.name, content=doc)
            photo.medium_thumb.save(name=doc.name, content=doc)
            photo.large_thumb.save(name=doc.name, content=doc)
            photo.save()
            # result_str = 'success upload {}'.format(photo.photo_hash)
        return HttpResponseRedirect(reverse('photos:photo_details', 
                                    kwargs={'pk': int(photo.pk)}))


class SearchView(FormView):
    form_class = forms.SearchForm
    template_name = 'photos/search_view.html'
    success_url = ''


class SearchResultsView(genViews.ListView):
    model = models.Photo
    context_object_name = 'photo_list'
    template_name = 'photos/medium_photo_list.html'
    paginate_by = 50

    def get_queryset(self):
        orig = models.Photo.objects.all()
        qs = models.Photo.objects.none()
        try:
            i = self.request.GET.getlist('owner')
            for ii in i:
                qs = qs | orig.filter(owner=ii)
        except MultiValueDictKeyError:
            pass        
        
        try:
            i = self.request.GET.getlist('events')
            # Start from empty photo qs
            pq = models.Photo.objects.none()
            for ii in i:
                # get photo from Event and EventTag
                e = models.Event.objects.get(id=int(ii))
                et = models.EventTag.objects.filter(atr=e)
                # add each photo to a qs
                for t in et:
                    pq |= models.Photo.objects.filter(id=t.photo.pk)

            # Union existing qs with events qs to get new qs
            qs = qs.union(pq)
        except MultiValueDictKeyError:
            pass        
        
        if len(self.request.GET) == 0:
            qs = orig

        return qs


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


# TODO: class LargePhotoListView(genViews.ListView):
class MediumPhotoListView(genViews.ListView):
    model = models.Photo
    context_object_name = 'photo_list'
    template_name = 'photos/medium_photo_list.html'
    paginate_by = 50


# ############### Autocompletes ####################
class PersonAC(ac.Select2QuerySetView):
    create_field = 'name'
    model = models.Person
    model_field_name = 'name'

    def has_add_permission(self, request):
        return True


class AnimalAC(ac.Select2QuerySetView):
    create_field = 'name'
    model = models.Animal
    model_field_name = 'name'

    def has_add_permission(self, request):
        return True


class LocationAC(ac.Select2QuerySetView):
    create_field = 'name'
    model = models.Location
    model_field_name = 'name'

    def has_add_permission(self, request):
        return True


class EventAC(ac.Select2QuerySetView):
    create_field = 'name'
    model = models.Event
    model_field_name = 'name'

    def has_add_permission(self, request):
        return True

