from datetime import datetime

from django.urls import path, register_converter

from .views import *


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('<int:user__pk>/', ConstructorByUser.as_view()),
    path('create/', ConstructorCreate.as_view()),
    path('detail/<int:pk>/', ConstructorDetail.as_view()),
    path('detail/<str:user__tg_token>/', ConstructorTokenDetail.as_view()),
    path('update/<int:pk>/', ConstructorUpdate.as_view()),

    path('staff/list/<int:const>/', StaffList.as_view()),
    path('staff/create/', StaffCreate.as_view()),
    path('staff/detail/<int:pk>/', StaffDetail.as_view()),
    path('staff/update/<int:pk>/', StaffUpdate.as_view()),
    path('staff/delete/<int:pk>/', StaffDelete.as_view()),

    path('category/list/<int:const>/', CategoryList.as_view()),
    path('category/create/', CategoryCreate.as_view()),
    path('category/<int:pk>/', CategoryDetail.as_view()),
    path('category/update/<int:pk>/', CategoryUpdate.as_view()),
    path('category/delete/<int:pk>/', CategoryDelete.as_view()),
    path('category/service/add/<int:service_pk>/<int:category_pk>', CategoryAddService.as_view()),
    path('category/staff/add/<int:staff_pk>/<int:category_pk>', CategoryAddStaff.as_view()),
    path('category/staff/del/<int:staff_pk>/<int:category_pk>', CategoryDelStaff.as_view()),

    path('service/list/<int:const>/', ServiceList.as_view()),
    path('service/create/', ServiceCreate.as_view()),
    path('service/detail/<int:pk>/', ServiceDetail.as_view()),
    path('service/update/<int:pk>/', ServiceUpdate.as_view()),
    path('service/delete/<int:pk>/', ServiceDelete.as_view()),
    path('service/staff/add/<int:service_pk>/<int:staff_pk>', ServiceAddStaff.as_view()),
    path('service/staff/delete/<int:service_pk>/<int:staff_pk>', ServiceDeleteStaff.as_view()),
    path('companytype/all/', CompanyTypeList.as_view()),

    path('event/', EventList.as_view()),
    path('event/<int:pk>/', EventDetail.as_view()),
    path('event/<yyyy:date>/<int:pk>/', EventDateList.as_view()),
    path('event/staff/list/<int:staff>/', EventStaffList.as_view()),

    path('image/create/', ImageCreate.as_view()),
    path('image/detail/<int:pk>/', ImageDetail.as_view()),

    path('bottext/list/<int:const>/', BotTextList.as_view()),
    path('bottext/<int:pk>/', BotTextDetail.as_view()),
    # path('bottext/<str:text_id>/<int:const>/', BotTextConstructor.as_view()),
    path('bottext/<str:text_id>/<str:const__user__tg_token>/', BotTextConstructor.as_view()),
]
