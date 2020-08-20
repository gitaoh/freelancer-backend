from rest_framework import serializers
from .models import User, Rating
import uuid


class UUIDGenerator:
    def __init__(self, model):
        self.model = model

    def generate_uuid(self):
        generate = uuid.uuid4()
        try:
            self.model.objects.get(uuid__exact=generate)
        except self.model.DoesNotExist as e:
            return generate
        else:
            self.generate_uuid()


def set_url(view_name, look_field):
    return serializers.HyperlinkedIdentityField(view_name=view_name, lookup_field=look_field)


excludeFields = ['first_name', 'last_name', 'groups', 'is_superuser', 'user_permissions', 'password', 'is_staff', ]


# User Serializer
class AuthUserSerializer(serializers.ModelSerializer):
    """
    Authorized/Authenticated User Serializer
    """

    class Meta:
        model = User
        fields = (
            'user_type', 'username', 'email', 'phone_number', 'terms', 'updates', 'is_active', 'createdAt', 'updatedAt')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer for the admin
    """

    class Meta:
        model = User
        exclude = ['first_name', 'last_name', 'groups', 'id', 'password', 'is_active']


# Register Serializer
class AuthRegisterSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Register user serializer
    """
    model = User

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        write_only_fields = ['password']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            uuid=self.generate_uuid())
        return user

    def update(self, instance, validated_data):
        super(AuthRegisterSerializer, self).update(instance, validated_data)


class AuthUserResetPasswordSerializer(serializers.Serializer):
    """
    Allow Client/User to reset their password
    """
    model = User

    old_password = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
    new_password = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)


class RatingModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serialize PaperType Model Objects to json format
    """
    model = Rating

    class Meta:
        model = Rating,
        exclude = ["deletedAt", 'client']

    def create(self, validated_data):
        return Rating.objects.create(
            client=self.context['request'].user,
            rate=int(validated_data['rate']),
            uuid=self.generate_uuid())
