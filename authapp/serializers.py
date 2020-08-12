from rest_framework import serializers
from .models import User


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
        # fields = '__all__'
        fields = ('user_type', 'username', 'email', 'phone_number', 'terms', 'updates', 'is_active','createdAt', 'updateAt')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer for the admin
    """

    # url = set_url(view_name='app:single-user', look_field='username')

    class Meta:
        model = User
        exclude = ['first_name', 'last_name', 'groups', 'id', 'password', 'is_active']


# Register Serializer
class AuthRegisterSerializer(serializers.ModelSerializer):
    """
    Register user serializer
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

    def update(self, instance, validated_data):
        print("validated_data")
        super(AuthRegisterSerializer, self).update(instance, validated_data)


class AuthUserResetPasswordSerializer(serializers.Serializer):
    """
    Allow Client/User to reset their password
    """
    model = User

    old_password = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
    new_password = serializers.CharField(max_length=128, required=True, allow_blank=False, allow_null=False)
