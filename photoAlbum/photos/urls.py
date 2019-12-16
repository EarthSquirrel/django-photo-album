from django.urls import path
from photos import views


app_name = 'photos'
urlpatterns = [
    path('upload-photo/', views.UploadPhotoView.as_view(), name='upload'),
    path('add-attributes/<photo_id>', views.AddAttributesView.as_view(),
         name='add_attributes'),
    # Autocomplete urls
    path('person-ac/', views.PersonAC.as_view(),
         name='person_ac'),
    path('animal-ac/', views.AnimalAC.as_view(),
         name='animal_ac'),
    path('location-ac/', views.LocationAC.as_view(),
         name='location_ac'),
    path('event-ac/', views.EventAC.as_view(),
         name='event_ac'),

]
