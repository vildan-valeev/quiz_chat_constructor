import requests
from rest_framework.serializers import ModelSerializer, Serializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Constructor, Service, Staff, Category, Event, Image, CompanyType, BotText
from rest_framework import serializers


# -----------------------
class BotTextSerializer(ModelSerializer):
    """ """

    class Meta:
        model = BotText
        fields = '__all__'


class BotTextLookupSerializer(ModelSerializer):
    """ """

    class Meta:
        model = BotText
        fields = '__all__'

    lookup_fields = ['text_id', 'const__user__tg_token']


# -----------------------
class CompanyTypeSerializer(ModelSerializer):
    """ """

    class Meta:
        model = CompanyType
        fields = '__all__'


class StaffSerializer(ModelSerializer):
    """" """

    class Meta:
        model = Staff
        fields = '__all__'


class StaffDetailSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffLookupSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        lookup_filed = 'const'


# -----------------------
class ServiceSerializer(ModelSerializer):
    """ """

    class Meta:
        model = Service
        fields = '__all__'


class ServiceDetailSerializer(ModelSerializer):
    """ """
    staff = StaffDetailSerializer(many=True)

    class Meta:
        model = Service
        fields = '__all__'


class ServiceLookupSerializer(ModelSerializer):
    """ """

    class Meta:
        model = Service
        fields = '__all__'
        lookup_filed = 'const'


# -----------------------
class CategorySerializer(ModelSerializer):
    """ """

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(ModelSerializer):
    """ """

    service = ServiceDetailSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryLookupSerializer(ModelSerializer):
    """ """
    service = ServiceSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'const'


class CategoryUpdateSerializer(ModelSerializer):
    """ """
    title = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Category
        fields = '__all__'


# -----------------------
class EventSerializer(ModelSerializer):
    """ """

    class Meta:
        model = Event
        fields = '__all__'


class EventStaffSerializer(ModelSerializer):
    """ """

    class Meta:
        model = Event
        fields = '__all__'
        lookup_field = 'staff'


# -----------------------

class ImageSerializer(ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )
    color = serializers.JSONField()

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        img = validated_data['image']
        f = img.file
        files = {'file': f}

        name = validated_data['name']
        url = 'http://colorz:7500/'
        color = requests.post(url=url, files=files, )
        img_model = Image(name=name, image=img, color=color.json())
        img_model.save()
        return img_model


# --------CONSTRUCTOR---------------
class ConstructorDetailSerializer(ModelSerializer):
    """ """

    class Meta:
        model = Constructor
        fields = '__all__'


class ConstructorSerializer(ModelSerializer):
    """ """
    logo = ImageSerializer(many=True)

    class Meta:
        model = Constructor
        fields = '__all__'


class ConstructorListSerializer(ModelSerializer):
    """ """
    logo = ImageSerializer(many=True)
    category = CategoryDetailSerializer(many=True)
    company_type = CompanyTypeSerializer(many=False)

    class Meta:
        model = Constructor
        fields = ['id', 'user', 'logo', 'company_type', 'name', 'custom_company_type',
                  'company_name', 'bot_name', 'color', 'construct', 'dialog_config', 'created', 'updated', 'category',
                  ]


class ConstructorTokenSerializer(ModelSerializer):
    """ """
    categories = CategoryDetailSerializer(many=True)

    class Meta:
        model = Constructor
        fields = ['id', 'user', 'categories', ]

    lookup_field = 'user__tg_token'


class ConstructorDetailLookupSerializer(ModelSerializer):
    """ """
    logo = ImageSerializer(many=True)
    company_type = CompanyTypeSerializer(many=False)

    class Meta:
        model = Constructor
        fields = ['id', 'user', 'logo', 'company_type', 'name', 'custom_company_type',
                  'company_name', 'bot_name', 'color', 'construct', 'dialog_config', 'created', 'updated', ]

    lookup_field = 'user__pk'
