from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .utils import get_time


def main_page(request):
    return render(request, "main.html")


# -----------------------
class ConstructorCreate(CreateAPIView):
    """Create constructor"""
    serializer_class = ConstructorDetailSerializer
    queryset = Constructor.objects.all()


class ConstructorDetail(RetrieveAPIView):
    serializer_class = ConstructorListSerializer
    queryset = Constructor.objects.all()


class ConstructorTokenDetail(RetrieveAPIView):
    serializer_class = ConstructorTokenSerializer
    queryset = Constructor.objects.all()
    lookup_field = 'user__tg_token'


class ConstructorUpdate(UpdateAPIView):
    serializer_class = ConstructorDetailSerializer
    queryset = Constructor.objects.all()
    http_method_names = ['patch', ]


class ConstructorByUser(RetrieveAPIView):
    serializer_class = ConstructorDetailLookupSerializer
    queryset = Constructor.objects.all()
    lookup_field = 'user__pk'


# -----------------------
class StaffList(ListAPIView):
    """Список сотрудников по id конструктора"""
    serializer_class = StaffLookupSerializer
    queryset = Staff.objects.all()
    lookup_field = 'const'


class StaffCreate(CreateAPIView):
    """Cоздание сотрудника с параметром конструктора. Конструктор обновляется(привязка сотрудника) автоматически"""
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    # def post(self, request, *args, **kwargs):
    #     print(args, )
    #     print(kwargs)
    #     serializer = StaffSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         c = Constructor.objects.get(pk=kwargs['constructor_pk'])
    #         print(serializer)
    #         c.staff.add(serializer.data.get('id'))
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDetail(RetrieveAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()


class StaffUpdate(UpdateAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    http_method_names = ['patch', ]


class StaffDelete(DestroyAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()


# --------------------------------------------------------------------
class CategoryList(ListAPIView):
    """Список всех категорий по id конструктора"""
    serializer_class = CategoryLookupSerializer
    queryset = Category.objects.all()
    lookup_field = 'const'


class CategoryCreate(CreateAPIView):
    """Создание специализации"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryUpdate(UpdateAPIView):
    serializer_class = CategoryUpdateSerializer
    queryset = Category.objects.all()
    http_method_names = ['patch', ]


class CategoryDelete(DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def delete(self, request, *args, **kwargs):
        # print(request.data)

        category = Category.objects.get(pk=kwargs['pk'])
        print(category.title)
        if category.title == 'Без категории':
            # print(args, kwargs)
            return Response(status=status.HTTP_400_BAD_REQUEST, data='"Без категории" удалять запрещено')
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAddService(APIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        # print(request.data)
        print(args, kwargs)
        old_categoryes = Category.objects.filter(service=kwargs['service_pk'])
        for i in old_categoryes:
            i.service.remove(kwargs['service_pk'])
        new_categoryes = Category.objects.filter(pk=kwargs['category_pk'])
        for i in new_categoryes:
            i.service.add(kwargs['service_pk'])
        return Response(status=status.HTTP_200_OK, data='Changed')


class CategoryAddStaff(APIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        # print(request.data)
        print(args, kwargs)
        all_categories = Category.objects.get(pk=kwargs['category_pk'])
        print(all_categories.service.values())
        for i in all_categories.service.all():
            i.staff.add(kwargs['staff_pk'])

        return Response(status=status.HTTP_200_OK, data='Added')


class CategoryDelStaff(APIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(args, kwargs)
        all_categories = Category.objects.get(pk=kwargs['category_pk'])
        # print(all_categories.service.values())
        for i in all_categories.service.all():
            i.staff.remove(kwargs['staff_pk'])

        return Response(status=status.HTTP_200_OK, data='Deleted')


# ----------SERVICE ----------
class ServiceList(ListAPIView):
    serializer_class = ServiceLookupSerializer
    queryset = Service.objects.all()
    lookup_field = 'const'


class ServiceCreate(CreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceDetail(RetrieveAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceUpdate(UpdateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    http_method_names = ['patch', ]


class ServiceDelete(DestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceAddStaff(APIView):
    """Привязываем сотрудника к новой услуге"""
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def post(self, request, *args, **kwargs):
        # print(request.data)
        print(args, kwargs)
        new_services = Service.objects.filter(pk=kwargs['service_pk'])
        for i in new_services:
            i.staff.add(kwargs['staff_pk'])
        return Response(status=status.HTTP_200_OK, data='Changed')


class ServiceDeleteStaff(APIView):
    """Отвязываем сотрудника от услуги"""
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def post(self, request, *args, **kwargs):
        # print(request.data)
        print(args, kwargs)
        service = Service.objects.get(pk=kwargs['service_pk'])

        service.staff.remove(kwargs['staff_pk'])
        return Response(status=status.HTTP_200_OK, data='Changed')


# -----------------------
class EventList(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventDateList(APIView):
    """
    Передаем дату, id сотрудника,
    получаем свободные даты записей
    """

    def get(self, request, pk, date, format=None):
        # print(pk, date)
        snippet = get_time(date, pk)
        # serializer = EventSerializer(snippet, many=True)

        # s = serializers.serialize('json', snippet)
        # print(serializer.data)
        # print(f'{snippet=}')
        return Response(snippet)


class EventDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    http_method_names = ['get', 'patch', 'delete']


class EventStaffList(ListAPIView):
    serializer_class = EventStaffSerializer
    model = serializer_class.Meta.model

    def get_queryset(self, ):
        return self.model.objects.filter(staff=self.kwargs['staff'])


class ImageCreate(CreateAPIView):
    """
    Example:
    {name: "name", image: "image"}
    """
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ImageDetail(RetrieveAPIView):
    """
    detail image by id
    """
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


# -----------------------
class BotTextDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = BotTextSerializer
    queryset = BotText.objects.all()
    http_method_names = ['get', 'patch', 'delete']


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class BotTextConstructor(MultipleFieldLookupMixin, RetrieveAPIView):
    """
        Передаем id тег сообщения, токен бота,
        получаем текст сообщения
    """
    serializer_class = BotTextLookupSerializer
    queryset = BotText.objects.all()
    lookup_fields = ['text_id', 'const__user__tg_token']



# -----------------------
class CompanyTypeList(ListAPIView):
    serializer_class = CompanyTypeSerializer
    queryset = CompanyType.objects.all()


class BotTextList(ListAPIView):
    """
    передаем id конструктора, получаем список сообщений
    """
    serializer_class = BotTextSerializer
    model = serializer_class.Meta.model

    def get_queryset(self, ):
        return self.model.objects.filter(const=self.kwargs['const'])
