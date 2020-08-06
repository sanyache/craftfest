from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('', index, name='index'),
    path('gallery',  GalleryList.as_view(), name='gallery_list'),
    path('image_gallery/<int:pk>', image_gallery, name='gallery_detail'),
    path('masters', MasterList.as_view(), name='master_list'),
    path('master_detail/<int:pk>', MasterDetail.as_view(), name='master_detail')
]