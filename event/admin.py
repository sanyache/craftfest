from django.contrib import admin
from .models import *

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
