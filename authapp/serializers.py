from rest_framework import serializers
from .models import User, Rating, Defaults, Avatar
from recycle.uuid_generator import UUIDGenerator


def set_url(view_name, look_field):
    return serializers.HyperlinkedIdentityField(view_name=view_name, lookup_field=look_field)


excludeFields = ['first_name', 'last_name', 'groups', 'is_superuser', 'user_permissions', 'password', 'is_staff']


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


class MakeAdminSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer for the admin
    """

    class Meta:
        model = User
        exclude = ['first_name', 'last_name', 'groups', 'id', 'password', 'is_active']


class MakeMaterAdminSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer for the admin
    """
    model = User

    class Meta:
        model = User
        exclude = ['first_name', 'last_name', 'groups', 'id', 'password', 'is_active']

    def update(self, instance, validated_data):
        return self.model.objects.update(user_type="MASTER")


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
        user = self.model.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=True,
            uuid=self.generate_uuid())
        return user

    def update(self, instance, validated_data):
        super(AuthRegisterSerializer, self).update(instance, validated_data)


class AuthUserResetPasswordSerializer(serializers.Serializer):
    """ Allow Client/User to reset their password """
    model = User

    old_password = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
    new_password = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)


class RatingModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    """ Serialize PaperType Model Objects to json format """
    model = Rating

    class Meta:
        model = Rating
        exclude = ['deletedAt', 'client', 'uuid']

    def create(self, validated_data):
        return Rating.objects.create(
            client=self.context['request'].user,
            rate=int(validated_data['rate']),
            uuid=self.generate_uuid())


class DefaultsModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    model = Defaults

    class Meta:
        model = Defaults
        exclude = ['deletedAt', 'uuid']

    def create(self, validated_data):
        return self.model.objects.create(
            **validated_data,
            uuid=self.generate_uuid(),
            user=self.context['request'].user)


class RetrieveDefaultsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defaults
        exclude = ['deletedAt']


class AvatarModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    """ Allow user/clients to create an avatar """
    model = Avatar

    class Meta:
        model = Avatar
        exclude = ['deletedAt', 'uuid', 'user', 'is_avatar']

    def create(self, validated_data):
        return self.model.objects.create(
            **validated_data,
            user=self.context['request'].user,
            uuid=self.generate_uuid(),
            is_avatar=True
        )


class RetrieveAvatarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        exclude = ['deletedAt']


class UpdateUserModelSerializer(serializers.ModelSerializer):
    """Allow a client/user to update their information"""

    class Meta:
        model = User
        fields = ['phone_number', 'updates']
