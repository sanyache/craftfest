from django.shortcuts import reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import *
from .utils import paginate
from craftfest.settings import ADMIN_EMAIL

import random, json

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


def get_short_product_list():

    categories = CategoryProduct.objects.all()
    products = []
    for category in categories:
        product_id = [i.id for i in Product.objects.filter(is_active=True, category=category)]
        random.shuffle(product_id)
        for id in product_id[:3]:
            products.append(id)
    product_list = Product.objects.filter(id__in=products).select_related('master', 'gallery')
    return product_list


def index(request):
    sliders = Slider.objects.all()
    schedule = Schedule.objects.all().order_by('time')
    schedule_paginate = paginate(schedule, 4, request, {}, var_name='schedule')
    gallery = Gallery.objects.filter(is_title=True).latest('created')
    gallery_list = list(gallery.photos.all())
    random.shuffle(gallery_list)
    gallery_list = gallery_list[:9]
    masters = list(Master.objects.all())
    random.shuffle(masters)
    masters = masters[:6]
    products = list(get_short_product_list())
    random.shuffle(products)
    products = products[:9]
    sponsors = Sponsor.objects.all()
    articles = Article.objects.filter(is_approve=True).order_by('-created')[:3]
    event = Event.objects.filter(is_active=True).order_by('-time').last()
    return render(request, 'index.html', {'sliders': sliders,
                                          'schedule': schedule_paginate,
                                          'gallery_list': gallery_list,
                                          'products': products,
                                          'masters': masters,
                                          'sponsors': sponsors,
                                          'articles': articles,
                                          'event': event})


def contact(request):

    if request.method == 'POST':
        contact_admin(request)
    return render(request, 'contact.html')


class ManagerList(ListView):
    """
    managers for about_us
    """
    model = Manager
    context_object_name = 'managers'
    template_name = 'about_us.html'


class ScheduleList(ListView):
    """
    full schedule list
    """
    model = Schedule
    queryset = Schedule.objects.all().order_by('time')
    context_object_name = 'schedule'
    template_name = 'schedule.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ScheduleList, self).get_context_data(object_list=None, **kwargs)
        context['event'] = Event.objects.filter(is_active=True).order_by('-time').last()
        return context


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

    def get_queryset(self):
        queryset = super(MasterList, self).get_queryset()
        if self.request.GET.get('name'):
            q = self.request.GET.get('name')
            queryset = Master.objects.filter(Q(last_name__icontains=q) |
                                             Q(first_name__icontains=q))
        return queryset


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


class ProductList(ListView):
    """
    class for rendering product list
    """
    model = Product
    queryset = get_short_product_list()
    # Product.objects.filter(is_active=True).select_related('master', 'gallery',
    #                                                                  'category')
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data(object_list=None, **kwargs)
        categories = CategoryProduct.objects.all()
        context['categories'] = categories
        return context


def product_list_by_category(request, pk):

    category = get_object_or_404(CategoryProduct, id=pk)
    categories = [category]
    products = Product.objects.filter(is_active=True, category=category).order_by('-created')
    context = paginate(products, 12, request, {}, var_name='products')
    context['categories'] = categories
    data = dict()
    data['html_form'] = render_to_string('includes/partial_product_list.html', context, request)
    return JsonResponse(data)


def product_list_by_master(request):
    if request.GET.get('name'):
        name = request.GET.get('name')
        try:
            last_name, first_name = name.split(' ')
            master = Master.objects.filter(last_name__iexact=last_name,
                                           first_name__iexact=first_name).first()
        except:
            master = Master.objects.filter(last_name__iexact=name).first()
        products = Product.objects.filter(master=master).order_by('-created')
        categories = master.category.all()
        context = paginate(products, 12, request, {}, var_name='products')
        context['categories'] = categories
        data = dict()
        data['html_form'] = render_to_string('includes/partial_product_list.html', context, request)
        return  JsonResponse(data)


class ProductDetail(DetailView):
    """
    class for rendering product's detail
    """
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class SearchMasterTypeahead(View):

    def get(self, request):
        q = request.GET.get('q', '')
        masters = Master.objects.filter(last_name__icontains= q)
        name_list = []
        for master in masters:
            new = {'q': master.get_full_name()}
            name_list.append(new)
        return HttpResponse(json.dumps(name_list), content_type="application/json")
