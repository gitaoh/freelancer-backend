from django.http import QueryDict
from django.shortcuts import render
from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework.generics import (
    RetrieveAPIView, ListAPIView, UpdateAPIView, GenericAPIView,
    DestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions.permissions import IsMiniAdmin, IsMasterAdmin, IsUser
from .serializers import (
    AuthUserSerializer, AuthRegisterSerializer, UserSerializer, AvatarModelSerializer, RetrieveAvatarModelSerializer,
    AuthUserResetPasswordSerializer, RatingModelSerializer, DefaultsModelSerializer, RetrieveDefaultsModelSerializer)
from django.contrib.auth import login, user_logged_in, update_session_auth_hash
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.response import Response
from .models import User, Rating, Defaults, Avatar


# Register API
class RegisterAPI(GenericAPIView):
    """
    Register a new user to the server
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user=user)
        return Response(
            {
                "user": AuthUserSerializer(user, context=self.get_serializer_context()).data,
                "token": token,
                "status": Response.status_code
            },
            status=Response.status_code, headers={
                'Status': Response.status_code
            })


class LoginAPI(KnoxLoginView):
    """
    Login a user to the server
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.active is False:
            """
            Deactivated users cannot log in
            """
            return Response(data={
                "success": 'Fail',
                "error": ['Deactivated'],
                "status": status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        # login a user
        login(request, user)

        # generate token for the user
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        return Response(data, status=Response.status_code, headers={
            "Status": Response.status_code
        })


class AuthUserAPIView(RetrieveAPIView):
    """
    :returns an authenticated user information
    Retrieve: Get user information
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser)
    serializer_class = AuthUserSerializer
    model = User
    http_method_names = ['get']

    def get_object(self):
        """
        A User should not be able to access their information if they are not active
        """
        queryset = self.model.objects.get(username=self.request.user, is_active=True)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                'user': serializer.data,
                'status': Response.status_code
            },
            status=Response.status_code,
            headers={
                "Status": Response.status_code
            }
        )


class UserApiView(ListAPIView):
    """Get all users of type user"""
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser | IsMiniAdmin | IsMasterAdmin, IsAuthenticated)
    model = User
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.all().filter(user_type="USER", is_active=True)
        return queryset


class UserUpdatePasswordApiView(UpdateAPIView):
    """
    update logged in user password
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser)
    model = User
    serializer_class = AuthUserResetPasswordSerializer
    http_method_names = ["put", "patch"]
    lookup_field = "username"

    def validate_current_password(self, serializer):
        # Check old password
        if not self.object.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        # set_password also hashes the password that the user will get
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()

        # make sure the user stays logged in
        update_session_auth_hash(self.request, self.object)

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }
        return Response(response)

    def get_object(self, queryset=None):
        queryset = self.model.objects.get(username=self.request.user, is_active=True)
        return queryset

    def convert_to_query_dict(self, ordinary_dict, *args, **kwargs):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)
        return query_dict

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return self.validate_current_password(serializer)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteApiView(DestroyAPIView):
    """
    DELETE: delete this users information
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser)
    serializer_class = AuthUserSerializer
    model = User
    lookup_field = "username"
    http_method_names = ["delete"]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "headers": {
                "Status": Response.status_code
            },
            'status': "Success",
            "message": "User successfully deleted.",
            'code': Response.status_code,
            "error_messages": []
        }, status=status.HTTP_204_NO_CONTENT, headers={"Status": Response.status_code})

    def perform_destroy(self, instance):
        instance.deactivate()


def robot(request):
    """
    Render the robots.txt file
    :param: request
    :return: render
    """
    return render(request, template_name='robots.txt', content_type='text/plain', status=Response.status_code)


# Todo User to Admin/Mater Api view

class MakeUserAdminAPIView(UpdateAPIView):
    """ Make a user an admin """
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    http_method_names = ['put', 'patch']
    model = User
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


class MakeAdminMasterAPIView(UpdateAPIView):
    """ Make an admin a master admin """
    http_method_names = ['put', 'patch']
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    model = User
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


"""
Allow user/clients to rate our work
Client can only CREATE rating
"""


class RatingCreateAPIView(CreateAPIView):
    """ Allow user/clients to rate our services """
    model = Rating
    serializer_class = RatingModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser)
    http_method_names = ['post']

    def get_queryset(self):
        self.model.objects.all()


"""
Defaults Model Views
User should be able to CREATE, UPDATE and RETRIEVE
"""


class CreateDefaultAPIView(CreateAPIView):
    """
    Allow a user to create some default fields
    """
    http_method_names = ['post']
    serializer_class = DefaultsModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsMasterAdmin, IsAuthenticated)
    model = Defaults

    def get_queryset(self):
        """ Query from data where users are active """
        return self.model.objects.all()

    def get_object(self):
        """ User should be active and should relate to the defaults """
        return self.model.objects.all().filter(user__is_active=True, user=self.request.user)


class UpdateDefaultsAPIView(UpdateAPIView):
    """ Allow a user/client to update their config """
    http_method_names = ['put', 'patch']
    permission_classes = (IsUser, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)
    model = Defaults
    serializer_class = DefaultsModelSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        """ Query from data where users are active and is related to user """
        return self.model.objects.all()


class RetrieveDefaultsAPIView(RetrieveAPIView):
    """ Allow a user/client to retrieve their default config """
    http_method_names = ['get']
    permission_classes = (IsUser, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)
    model = Defaults
    serializer_class = RetrieveDefaultsModelSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        """ Query from data where users are active """
        return self.model.objects.all().filter(user__is_active=True)


class AvatarCreateAPIView(CreateAPIView):
    """ Upload an avatar to the server """
    http_method_names = ['post']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsMasterAdmin, IsAuthenticated)
    serializer_class = AvatarModelSerializer
    model = Avatar

    def get_queryset(self):
        return self.model.objects.all()


class UpdateAvatarAPIView(UpdateAPIView):
    """ Allow user to retrieve their avatar link """
    http_method_names = ['put', 'patch']
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    authentication_classes = (TokenAuthentication,)
    serializer_class = AvatarModelSerializer
    model = Avatar
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.model.objects.all()


class RetrieveAvatarAPIView(RetrieveAPIView):
    """ Allow user to retrieve their avatar link """
    http_method_names = ['get']
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    authentication_classes = (TokenAuthentication,)
    serializer_class = RetrieveAvatarModelSerializer
    model = Avatar
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.model.objects.all()
