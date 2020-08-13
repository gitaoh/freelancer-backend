import uuid as uu
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers
from .models import (
    Discipline,
    Order,
    PaperType,
    Notification,
    OrderFiles
)
from rest_framework import exceptions

excludeFields = ['first_name', 'last_name', 'groups', 'is_superuser', 'user_permissions', 'password', 'is_staff']


def send_email(user, status, header):
    email = user.email
    username = user.username
    html_message = render_to_string('app/Email/custome2.html', {'user': username, 'header': header})
    plain_message = strip_tags(html_message)
    from_email = "no-reply@dpao.com"
    send_mail(subject=status, message=plain_message, recipient_list=[email],
              from_email=from_email, html_message=html_message)


def set_url(view_name, look_field):
    return serializers.HyperlinkedIdentityField(view_name=view_name, lookup_field=look_field)


def uuid_func(kwargs):
    if kwargs['context']['request'].method == "POST":
        try:
            kwargs['data']['uuid']
        except Exception as e:
            kwargs['data']['uuid'] = uu.uuid4()


class NotificationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = Notification
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        uuid_func(kwargs=kwargs)
        super(NotificationSerializer, self).__init__(*args, **kwargs)


class PaperTypeSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = PaperType
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        uuid_func(kwargs=kwargs)
        super(PaperTypeSerializer, self).__init__(*args, **kwargs)


class OrderFilesSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = OrderFiles
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        uuid_func(kwargs=kwargs)
        super(OrderFilesSerializer, self).__init__(*args, **kwargs)


class DisciplineSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = Discipline
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        uuid_func(kwargs=kwargs)
        super(DisciplineSerializer, self).__init__(*args, **kwargs)


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise exceptions.ValidationError("Unable to login with given credentials")


class OrderSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        uuid_func(kwargs=kwargs)
        super(OrderSerializer, self).__init__(*args, **kwargs)
