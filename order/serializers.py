from rest_framework import serializers
from order.models import Order, Files, Notification


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the order model
    """

    class Meta:
        model = Order
        fields = "__all__"


class OrderFilesSerializer(serializers.ModelSerializer):
    """
    serializer for the orderFiles model
    """

    # uuid = serializers.UUIDField()

    class Meta:
        model = Files
        fields = "__all__"
    #
    # def __init__(self, *args, **kwargs):
    #     uuid_func(kwargs=kwargs)
    #     super(OrderFilesSerializer, self).__init__(*args, **kwargs)


class NotificationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = Notification
        fields = "__all__"
