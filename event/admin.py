from django.contrib import admin
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):

    model = Slider


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    model = Schedule
    list_display = ('time', 'short_description')


class ImageGalleryInLine(admin.TabularInline):
    """
    for show foreign key dependence
    """
    model = ImageGallery
    fields = ('image',)
    extra = 0


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    """
    class for model CategoryGallery
    """
    list_display = ('name',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """
    class for model Gallery
    """

    model = Gallery
    list_display = ('title','category', 'is_title', 'created')
    inlines = [ImageGalleryInLine]


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    """
    class for model Master
    """
    list_display = ('last_name', 'first_name')
    ordering = ['last_name']
    list_filter = ['last_name']


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):

    list_display = ['title']


class ArticleAdminForm(forms.ModelForm):
    """
    form for article model with ckeditor
    """
    content = forms.CharField(label="контент", widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'is_approve', 'created')
    list_display_links = ('title',)
    form = ArticleAdminForm
