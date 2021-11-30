from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from constructor.models import Constructor, Staff, Category, Service, BotText, DefaultStaff, \
    DefaultCategory


# @disable_for_loaddata
@receiver(pre_save, sender=Constructor)
def check_edit_id(sender, instance: Constructor, **kwargs):
    if kwargs.get('raw', False):
        return False

    if instance.id is None:  # new object will be created
        return False  # write your code here
    else:
        previous = Constructor.objects.get(pk=instance.pk)
        if previous.company_type != instance.company_type:  # field will be updated

            # очищаем конструктор
            Staff.objects.filter(const=instance).delete()
            Service.objects.filter(const=instance).delete()
            Category.objects.filter(const=instance).delete()

            if hasattr(instance.company_type, 'pk'):  # проверка есть ли атрибут рк у company type

                def_category = DefaultCategory.objects.filter(company_type=instance.company_type.id)

                def_staff = DefaultStaff.objects.filter(company_type=instance.company_type.id)
                for c in def_category:
                    category_inst, created = Category.objects.get_or_create(title=c.title,
                                                                            const=instance)
                    for sv in c.service.values():  # достаем привязанные услуги к категории
                        service_inst, created = Service.objects.get_or_create(name=sv['name'],
                                                                              price=sv['price'],
                                                                              duration=sv['duration'],
                                                                              const=instance, )
                        category_inst.service.add(service_inst)
                        serv_staff = c.service.get(pk=sv['id'])  # достаем привязанные сотрудники к услуге
                        for st in serv_staff.staff.values():
                            staff_inst, created = Staff.objects.get_or_create(name=st['name'], const=instance)
                            service_inst.staff.add(staff_inst)


@receiver(post_save, sender=Constructor)
def save_const(sender, instance: Constructor, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        Category.objects.get_or_create(title='Без категории',
                                       const=instance)  # добавляем дефолтную категорию в конструктор
        for i in BotText.objects.filter(const_id=None):
            BotText.objects.create(text=i.text, text_id=i.text_id, const=instance)

    # TODO: при создании конструктора, создать телеграм бота


@receiver(pre_delete, sender=Category)
def save_const(sender, instance: Category, **kwargs):
    if kwargs.get('raw', False):
        return False
    if instance.title == 'Без категории':
        return False
    uncat = Category.objects.filter(const=instance.const, title='Без категории')
    print(instance.service.values())
    print(uncat)
    for i in instance.service.values():
        print(i['id'])
        for u in uncat:
            u.service.add(i['id'])


@receiver(post_save, sender=Service)
def save_const(sender, instance: Service,created,  **kwargs):
    if kwargs.get('raw', False):
        return False
    print('добавление услуги к без категории')
    if created:
        uncat = Category.objects.filter(const=instance.const, title='Без категории')
        for i in uncat:
            i.service.add(instance)
        # TODO:  создании услуги, создавать кнопку
