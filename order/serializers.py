from rest_framework import serializers
from recycle.uuid_generator import UUIDGenerator
from order.models import Order, Files, Message, Cancel, Writer
from authapp.models import User
import random
from app.choices import AdminCategory
from uuid import UUID
from knox.models import AuthToken

def order_id_generator():
    # FrontLetters
    letters = ['A', 'B', 'C', 'D', 'E']
    random.shuffle(letters)
    length = range(1000000)  # max_length
    number = random.sample(length, 1)  # one count
    _id = f'#{letters[0]}{str(letters[1]).lower()}-{number[0]}'  # generate
    try:
        # Unique violation checker
        Order.objects.all().get(uuid__exact=_id)
    except Order.DoesNotExist as e:
        return _id
    else:
        # Recurse if card_number exists
        order_id_generator()


class OrderSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serializer for the order model
    """
    model = Order

    class Meta:
        model = Order
        exclude = ['writer', 'deletedAt', 'payments_url', 'confirmed', 'revision', 'dispute', 'paid', 'uuid', 'user',
                   'card', 'additional_materials', 'deleted_by']

    """
    # Writer = is being set
    # user = Current Request User
    ✔ card = Required but generated
    ✔ paper_type = Required
    ✔ discipline = Required
    ✔ title = Required
    ✔ instructions = Required
    deadline = required 
    cost = required 
    paid = required 
    payment = required but hidden
    academic = required but has to be under the choices set
    format = required but has to be under the choices set
    spacing = required but has to be under the choices set
    preference = required but has to be under the choices set
    ✔ additional_material = not required but can be set/updated to include
    
    ppt = no required
    status = Auto set
    pages = not required since its clients choice 
    sources = not required since its clients choice 
    charts = not required since its clients choice 
    native = not required since its clients choice 
    progressive = not required since its clients choice
    smart = not required since its clients choice
    rate = not required since its clients choice
    """

    def create(self, validated_data):
        files = []
        if validated_data['additional_materials']:
            files = validated_data.pop('additional_materials')
        instance = self.model.objects.create(**validated_data, user=self.context['request'].user,
                                             uuid=self.generate_uuid(), card=order_id_generator())
        if validated_data['additional_materials']:
            instance.additional_materials = files
        return instance


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['deletedAt', 'card', 'uuid', 'user', 'deleted_by']


class OrderFilesSerializer(serializers.ModelSerializer):
    """
    serializer for the orderFiles model
    """

    class Meta:
        model = Files
        fields = "__all__"


class SetOrderWriterSerializer(serializers.Serializer):
    """Assign an order to a writer"""

    # Todo Make a request with this
    # Todo ensure admin endpoint to retrieve order and writer includes their #UUID

    order = serializers.UUIDField(required=True, allow_null=False)
    writer = serializers.UUIDField(required=True, allow_null=False)


class CancelModeSerializer(serializers.ModelSerializer, UUIDGenerator):
    model = Cancel

    class Meta:
        model = Cancel
        exclude = ['uuid', 'deletedAt', 'user', 'is_active']

    # Todo order_id will be for the order being canceled
    def create(self, validated_data):
        return self.model.objects.create(
            reason=validated_data['reason'],
            order=Order.objects.all().get(uuid__exact=UUID(str(validated_data['order']))),
            uuid=self.get_fields(),
            user=self.context['request'].user
        )


class MessageModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Allow client and admin to communicate through messages
    """
    model = Message

    class Meta:
        model = Message
        fields = ['title', 'content', 'user', 'order']

    def create(self, validated_data):
        return Message.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            uuid=self.generate_uuid(),
            order=Order.objects.get(is_paper=True, uuid__exact=str(validated_data['order'])),
            user=User.objects.get(is_active=True, is_superuser=False, is_staff=False,
                                  username__exact=str(validated_data['user']), user_type=AdminCategory.USER),
            admin=User.objects.get(is_active=True, is_superuser=True, is_staff=False,
                                   username__exact=str(validated_data['admin']))
        )


class RetrieveWriterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['uuid', 'first_name', 'last_name', 'username', 'level', 'bio', 'createdAt', 'updatedAt']


class WriterModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    model = Writer

    class Meta:
        model = Writer
        fields = ['username', 'level', 'first_name', 'last_name', 'email', 'bio']

    def create(self, validated_data):
        return self.model.objects.create(
            **validated_data,
            uuid=self.generate_uuid()
        )
