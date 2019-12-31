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

    
    def add_atribute(self, model, tag, atrs, photo):
        if len(atrs) > 0:
            for atr in atrs:
                #atr = model.objects.get(id=i)
                tag.objects.get_or_create(photo=photo, atr=atr)
                
    def form_valid(self, form):
        photo_id = self.kwargs['photo_id']
        photo = models.Photo.objects.get(id=photo_id)
        data = form.cleaned_data
        keys = [['events', models.EventTag, models.Event], 
                ['animals', models.AnimalTag, models.Animal],
                ['location', models.LocationTag, models.Location],
                ['people', models.PersonTag, models.Person],
                ['classifiers', models.ClassifierTag, models.Classifier]
               ]
        
        for key in keys:
            self.add_atribute(key[2], key[1], data[key[0]], photo)
        
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
            create_date = utils.get_DateTimeOriginal(doc.path)
            if create_date != '':
                photo.create_date = create_date
                photo.metadata = True
            # Do backup things
            photo.backup_path = utils.save_backup(doc.name, doc.path)
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
    
    def search_mt(self, key, model, tag, qs):
        try:
            # Get list in specific search field
            li = self.request.GET.getlist(key)
            # check if length > 0, if not return
            if not len(li) > 0:
                return qs
            # holdes all the photos with the tags in search
            tag_pq = models.Photo.objects.none()
            # 
            for i in li:
                # get photo from Model and ModelTag
                m = model.objects.get(id=int(i))
                t = tag.objects.filter(atr=m)
                # for each tag model in list, add photo to a qs
                for tt in t:
                    tag_pq |= models.Photo.objects.filter(id=tt.photo.pk)
            # union existing qs with tag qs to get new qs
            qs = qs.intersection(tag_pq)
        except MultiValueDictKeyError:
            pass
        return qs

    def get_queryset(self):
        qs = models.Photo.objects.all()
        try:
            i = self.request.GET.getlist('owner')
            if len(i) > 0:
                oqs = models.Photo.objects.none()
                for ii in i:
                    oqs = oqs | qs.filter(owner=ii)
                qs = qs.intersection(oqs)
        except MultiValueDictKeyError:
            pass        
        ModelTag = [['events', models.Event, models.EventTag],
                    ['animals', models.Animal, models.AnimalTag]
                   ]

        # key model tag qs
        for mt in ModelTag:
            qs = self.search_mt(mt[0], mt[1], mt[2], qs)


        return qs.order_by('create_date')


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

    def get_queryset(self):
        return models.Photo.objects.all().order_by('create_date')


# ############### Autocompletes ####################
class PersonAC(ac.Select2QuerySetView):
    create_field = 'name'
    model = models.Person
    model_field_name = 'name'

    def has_add_permission(self, request):
        return True


class DeviceAC(ac.Select2QuerySetView):
    create_field = 'name'
    model = models.Device
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

