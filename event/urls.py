from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('', index, name='index'),
    path('contact_admin', contact_admin, name='contact_admin'),
    path('contact', contact, name='contact'),
    path('schedule', ScheduleList.as_view(), name='schedule_list'),
    path('gallery',  GalleryList.as_view(), name='gallery_list'),
    path('image_gallery/<int:pk>', image_gallery, name='gallery_detail'),
    path('masters', MasterList.as_view(), name='master_list'),
    path('master_detail/<int:pk>', MasterDetail.as_view(), name='master_detail'),
    path('articles', ArticleList.as_view(), name='article_list'),
    path('article_detail/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('about_us', ManagerList.as_view(), name='about_us'),
    path('product_list', ProductList.as_view(), name='product_list'),
    path('product_by_category/<int:pk>', product_list_by_category, name='product_by_category'),
    path('product_detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('search_master_typeahead', SearchMasterTypeahead.as_view(), name='search_master_typeahead'),
    path('product_list_by_master', product_list_by_master, name='product_list_by_master'),
]