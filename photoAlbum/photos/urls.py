from django.urls import path
from photos import views


app_name = 'photos'
urlpatterns = [
    path('upload-photo/', views.UploadPhotoView.as_view(), name='upload'),
    path('add-attributes/<photo_id>', views.AddAttributesView.as_view(),
         name='add_attributes'),
]
