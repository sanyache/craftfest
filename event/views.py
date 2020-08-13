from django.shortcuts import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .models import *
from .utils import paginate
from craftfest.settings import ADMIN_EMAIL

import random

# Create your views here.


def contact_admin(request):
    if request.method == 'POST':
        if request.POST['name'] and request.POST['message'] and request.POST['email']:
            name = request.POST['name']
            message = request.POST['message']
            from_email = request.POST['email']
            try :
                send_mail('Для контакту з адміном сайту',
                          'Отримано лист від {} {} {}'.format(name, from_email, message),
                          ADMIN_EMAIL, [ADMIN_EMAIL, 'kraftfest@ukr.net'])
            except Exception as e:
                print(e)
            return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))


def index(request):
    sliders = Slider.objects.all()
    schedule = Schedule.objects.all().order_by('time')
    schedule_paginate = paginate(schedule, 4, request, {}, var_name='schedule')
    gallery = Gallery.objects.filter(is_title=True).latest('created')
    gallery_list = list(gallery.photos.all())
    random.shuffle(gallery_list)
    gallery_list = gallery_list[:12]
    masters = list(Master.objects.all())[:6]
    random.shuffle(masters)
    masters = masters[:6]
    sponsors = Sponsor.objects.all()
    articles = Article.objects.filter(is_approve=True).order_by('-created')[:3]
    event = Event.objects.filter(is_active=True).order_by('-time').last()
    return render(request, 'index.html', {'sliders': sliders,
                                          'schedule': schedule_paginate,
                                          'gallery_list': gallery_list,
                                          'masters': masters,
                                          'sponsors': sponsors,
                                          'articles': articles,
                                          'event': event})


def contact(request):

    if request.method == 'POST':
        contact_admin(request)
    return render(request, 'contact.html')


class ScheduleList(ListView):
    """
    full schedule list
    """
    model = Schedule
    queryset = Schedule.objects.all().order_by('time')
    context_object_name = 'schedule'
    template_name = 'schedule.html'


class GalleryList(ListView):
    """
    view for rendering gallery list
    """
    model = Gallery
    queryset = Gallery.objects.exclude(category='product')
    context_object_name = 'galleries'
    template_name = 'gallery.html'


def image_gallery(request, pk):
    """
    view for rendering photo gallery
    """
    gallery = get_object_or_404(Gallery, id=pk)
    photos = ImageGallery.objects.filter(gallery=gallery)
    context = paginate(photos, 12, request, {}, var_name='photos')
    context['gallery'] = gallery
    return render(request, 'gallery_detail.html', context)


class MasterList(ListView):
    """
    view for rendering masters
    """
    model = Master
    context_object_name = 'masters'
    template_name = 'masters.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MasterList, self).get_context_data(object_list=None, **kwargs)
        categories = CategoryProduct.objects.all()
        context['categories'] = categories
        return context


class MasterDetail(DetailView):
    """
    class for rendering details about master
    """
    model = Master
    template_name = 'master-detail.html'
    context_object_name = 'master'

    def get_context_data(self, **kwargs):
        context = super(MasterDetail, self).get_context_data(**kwargs)
        if self.object.gallery:
            photos = ImageGallery.objects.filter(gallery=self.object.gallery)
            context = paginate(photos, 9, self.request, context, var_name='photos')
        return context


class ArticleList(ListView):
    """
    class for rendering article list
    """
    model = Article
    queryset = Article.objects.filter(is_approve=True)
    template_name = 'articles.html'
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    """
    class for rendering article by <pk>
    """
    model = Article
    template_name = 'single-article.html'
    context_object_name = 'article'
