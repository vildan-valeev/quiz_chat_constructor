from django.contrib.contenttypes.models import ContentType
from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField

from users.models import UserAccount


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    color = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class BotText(models.Model):
    text = models.TextField(max_length=300, )
    text_id = models.CharField(max_length=255, verbose_name='Название- идентификатор',
                               help_text='на англ, без пробелов, с нижним подчеркиванием')

    const = models.ForeignKey('Constructor', on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name='Конструктор')
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, )
    updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __str__(self):
        return str(self.text)

    class Meta:
        ordering = ['id']
        verbose_name = 'Сообщение бота'
        verbose_name_plural = 'Сообщения бота'


class CompanyType(models.Model):
    name = models.CharField(max_length=100, null=True, )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Тип компании'
        verbose_name_plural = 'Типы компаний'


class Constructor(models.Model):
    name = models.CharField(max_length=140, null=True, verbose_name='Заголовок', blank=True,)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    logo = models.ManyToManyField(Image, blank=True, related_name='constructors')
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Вид деятельности')
    custom_company_type = models.CharField(max_length=140, null=True, blank=True, verbose_name='Кастомный тип компании')
    company_name = models.CharField(max_length=140, null=True, blank=True, verbose_name='Компания')
    bot_name = models.CharField(max_length=140, null=True, blank=True, verbose_name='Имя бота')
    color = models.JSONField(null=True, blank=True, verbose_name='Цвет')
    construct = models.JSONField(blank=True, null=True)
    dialog_config = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, )
    updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Конструктор'
        verbose_name_plural = 'Конструкторы'

    def __str__(self):
        return str(f'{self.id} | {self.name}')


class Category(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    service = models.ManyToManyField('Service', blank=True, verbose_name='Услуги', )
    const = models.ForeignKey(Constructor, on_delete=models.CASCADE, blank=True,
                              verbose_name='Конструктор', null=True, related_name='categories')

    # callback = models.CharField(max_length=300, verbose_name='Название')

    class Meta:
        ordering = ['id']
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #


class Service(models.Model):
    name = models.CharField(max_length=300, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена', default=0)
    duration = models.TimeField(blank=True, null=True)
    staff = models.ManyToManyField('Staff', blank=True, verbose_name='Сотрудники')
    const = models.ForeignKey(Constructor, on_delete=models.CASCADE, blank=True,
                              verbose_name='Конструктор', null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=300, null=True, verbose_name='Имя')
    const = models.ForeignKey(Constructor, on_delete=models.CASCADE, blank=True,
                              verbose_name='Конструктор', null=True, related_name='staffs')

    class Meta:
        ordering = ['id']
        verbose_name = 'Сотрудника'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICE = [
        ('FR', 'Free'),
        ('BS', 'Busy'),
    ]

    name = models.CharField(max_length=300, verbose_name='Название')
    details = models.TextField(max_length=300, verbose_name='Описание', null=True)
    color = models.CharField(max_length=300, verbose_name='Цвет', default='#000')
    status = models.CharField(max_length=300, verbose_name='Статус', default='FR', choices=STATUS_CHOICE)
    price = models.IntegerField(verbose_name='Цена', null=True)
    phone = models.CharField(max_length=300, verbose_name='Номер телефона', null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True,
                              verbose_name='Сотрудник', null=True, related_name='events')

    start = models.DateTimeField(verbose_name='Начало приема',)
    end = models.DateTimeField(verbose_name='Окончание приема')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class DefaultCategory(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название', )
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Тип компании')
    service = models.ManyToManyField('DefaultService', blank=True, verbose_name='Услуги')

    class Meta:
        ordering = ['id']
        verbose_name = 'Стандартную Категорию'
        verbose_name_plural = 'Стандартные Категории'

    def __str__(self):
        return self.title


class DefaultService(models.Model):
    name = models.CharField(max_length=300, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена', default=0)
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Тип компании')
    duration = models.TimeField(blank=True, null=True)
    staff = models.ManyToManyField('DefaultStaff', blank=True, verbose_name='Сотрудники')

    class Meta:
        ordering = ['id']
        verbose_name = 'Стандартную Услугу'
        verbose_name_plural = 'Стандартные Услуги'

    def __str__(self):
        return self.name


class DefaultStaff(models.Model):
    name = models.CharField(max_length=300, null=True, verbose_name='Имя')
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Тип компании')

    class Meta:
        ordering = ['id']
        verbose_name = 'Стандарного Сотрудника'
        verbose_name_plural = 'Стандартные Сотрудники'

    def __str__(self):
        return f'{self.name} | {self.company_type}'

# TODO: when delete Foo, move related Bar instances to another Foo instance
# class Foo(models.Model):
#     title = models.CharField(max_length=300, verbose_name='Название')
#     bar = models.ManyToManyField('Bar', )
#
#     # def __del__(self):
#
#
# class Bar(models.Model):
#     name = models.CharField(max_length=300, verbose_name='Название')
