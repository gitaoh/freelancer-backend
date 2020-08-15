from rest_framework import serializers
from order.models import Order, OrderFiles


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
        model = OrderFiles
        fields = "__all__"
    #
    # def __init__(self, *args, **kwargs):
    #     uuid_func(kwargs=kwargs)
    #     super(OrderFilesSerializer, self).__init__(*args, **kwargs)
