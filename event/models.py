from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, Transpose, SmartResize

# Create your models here.


class Slider(models.Model):
    """
    class for slider in header
    """
    title = models.CharField(max_length=250, verbose_name='опис')
    image = models.ImageField(upload_to='slider/', verbose_name='фото для слайдеру')
    slider_image = ImageSpecField(source='image',
                                  processors=[Transpose(), SmartResize(1920, 730)],
                                  format='JPEG',
                                  options={'quality': 100})

    class Meta:
        verbose_name = 'Слайдер'

    def __str__(self):
        return "{}".format(self.title)


class Schedule(models.Model):
    """
    class for schedule
    """
    time = models.CharField(max_length=15, verbose_name='час')
    short_description = models.CharField(max_length=125, verbose_name='короткий опис')
    description = models.TextField(verbose_name='опис')

    class Meta:
        verbose_name = 'захід в програмі'
        verbose_name_plural = 'Програма'

    def __str__(self):
        return "{} {}".format(self.time, self.short_description)


class Gallery(models.Model):
    """
    class  describe Gallery
    """

    CATEGORY_GALLERY = (
        ('fest', 'Фестиваль'),
        ('event', 'Захід'),
        ('product', 'Продукція')
    )
    title = models.CharField(max_length=125, verbose_name='назва альбому')
    category = models.CharField(max_length=15, choices=CATEGORY_GALLERY,
                                verbose_name='категорія альбому')
    title_image = models.ImageField(upload_to='title/',
                                    verbose_name='титульне фото',
                                    blank=True, null=True)
    title_image_avatar = ImageSpecField(source='title_image',
                                        processors=[Transpose(), SmartResize(370, 280)],
                                        format='JPEG',
                                        options={'quality': 60})
    title_image_big = ImageSpecField(source='title_image',
                                     processors=[Transpose(), SmartResize(1800, 950)],
                                     format='JPEG',
                                     options={'quality': 100})
    description = models.CharField(max_length=250, blank=True, verbose_name='опис альбому')
    is_title = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True, verbose_name='створено')

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = "Галереї"

    def __str__(self):
        return "{}".format(self.title)


class ImageGallery(models.Model):
    """
    class describe photo for gallery
    """
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', verbose_name='фото')
    image_avatar = ImageSpecField(source='image',
                                  processors=[Transpose(), SmartResize(370, 280)],
                                  format='JPEG',
                                  options={'quality': 60})
    image_big = ImageSpecField(source='image',
                               processors=[Transpose(), ResizeToFit(1800, 950)],
                               format='JPEG',
                               options={'quality': 90})
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name='галерея',
                                related_name='photos')

    class Meta:
        verbose_name = "Фото галереї"
        verbose_name_plural = "Фото галереї"
        ordering = ['id']


class CategoryProduct(models.Model):
    """
    class describe category for master's product
    """
    name = models.CharField(max_length=125)

    class Meta:
        verbose_name = 'Категорія продукції'
        verbose_name_plural = 'Категорії продукції'

    def __str__(self):
        return "{}".format(self.name)


class Master(models.Model):
    """
    class describe master that take part in fest
    """
    first_name = models.CharField(max_length=125, verbose_name="ім'я")
    last_name = models.CharField(max_length=125, verbose_name='прізвище')
    image = models.ImageField(upload_to='master/', verbose_name='фото')
    image_avatar = ImageSpecField(source='image',
                                  processors=[Transpose(), SmartResize(570, 570)],
                                  format='JPEG',
                                  options={'quality': 70})
    image_masters = ImageSpecField(source='image',
                                   processors=[Transpose(), SmartResize(285, 300)],
                                   format='JPEG',
                                   options={'quality': 70})
    category = models.ManyToManyField(CategoryProduct, related_name='masters', blank=True)
    phone = models.CharField(max_length=15, verbose_name="телефон", blank=True, null=True)
    facebook = models.CharField(max_length=100, verbose_name="фейсбук", blank=True, null=True)
    instagram = models.CharField(max_length=100, verbose_name="інстаграм", blank=True, null=True)
    site = models.CharField(max_length=100, verbose_name="сайт", blank=True, null=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name="gallery_master")
    short_description = models.CharField(max_length=350, verbose_name='короткий опис',
                                         blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name='повний опис')

    def get_full_name(self):
        return "{} {}".format(self.last_name, self.first_name)

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Майстер'
        verbose_name_plural = 'Майстри'


class Manager(models.Model):
    """
    class describe manager who server for fest
    """
    first_name = models.CharField(max_length=125, verbose_name="ім'я")
    last_name = models.CharField(max_length=125, verbose_name='прізвище')
    middle_name = models.CharField(max_length=125, verbose_name='по -батькові', default='')
    image = models.ImageField(upload_to='manager/', verbose_name='фото')
    duty = models.TextField(blank=True, null=True, verbose_name='відповідальний за')

    def get_full_name(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджери'


class Sponsor(models.Model):
    """
    class describe sponsor
    """
    title = models.CharField(max_length=125, blank=True, verbose_name='назва')
    site = models.CharField(max_length=150, blank=True, null=True, verbose_name='сайт')
    image = models.ImageField(upload_to='sponsor/', verbose_name='фото')
    image_avatar = ImageSpecField(source='image',
                                  processors=[Transpose(), SmartResize(250, 205)],
                                  format='JPEG',
                                  options={'quality': 70})

    class Meta:
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсори'

    def __str__(self):
        return "{}".format(self.title)


class Article(models.Model):
    """
    model that describe post
    """
    title = models.CharField(max_length=125, verbose_name='Заголовок')
    description = models.CharField(max_length=250, verbose_name='Короткий опис')
    content = models.TextField(blank=True, verbose_name='контент')
    created = models.DateTimeField(auto_now_add=True, verbose_name='створено')
    image = models.ImageField(upload_to='article/', null=True, blank=True, verbose_name='фото')
    image_avatar = ImageSpecField(source='image',
                                  processors=[Transpose(), SmartResize(360, 250)],
                                  format='JPEG',
                                  options={'quality': 60})
    image_grid = ImageSpecField(source='image',
                                processors=[Transpose(), SmartResize(750, 750)],
                                format='JPEG',
                                options={'quality': 80})
    is_approve = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'


class Event(models.Model):
    """
    class describe event's time and place
    """
    title = models.CharField(max_length=200, verbose_name='назва заходу', blank=True)
    place = models.CharField(max_length=200, verbose_name='місце проведення', blank=True)
    time = models.DateTimeField(blank=True, null=True, verbose_name='дата проведення')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Час і місце'

    def __str__(self):
        return "{} {}".format(self.title, self.time)
