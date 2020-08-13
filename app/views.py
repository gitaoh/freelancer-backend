from knox.auth import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveDestroyAPIView,
    ListCreateAPIView, RetrieveAPIView, )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.models import Order, OrderFiles
from app.serializers import OrderSerializer, OrderFilesSerializer
from authapp.permissions.permissions import IsMiniAdmin, IsUser, IsMasterAdmin


class OrderApiView(CreateAPIView):
    """
    POST: Create a new order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsAdminUser | IsMasterAdmin)
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["post"]

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset


class UsersSpecificOrders(ListAPIView):
    """
    Get User Specific Order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsAdminUser | IsMasterAdmin)
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user.id, is_paper=True)


class GetOrdersApiView(ListAPIView):
    """
    List: list of all order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMiniAdmin | IsAdminUser | IsMasterAdmin)
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class OrderUpdateApiView(UpdateAPIView):
    """
    Retrieve: get the information of a single order
    PUT: update order information
    PATCH: partial update to order information
    """
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["put", 'patch']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser, IsMiniAdmin, IsMasterAdmin)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user.id, is_paper=True)


class OrderDeleteApiView(DestroyAPIView):
    """
    Retrieve: get the information of a single order
    Delete: delete an order
    """
    model = Order
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser)
    http_method_names = ['delete']
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user.id, is_paper=True)


class SingleTOAdminsOrderApiView(RetrieveAPIView):
    """
    Retrieve: get the information of a single order as an admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser | IsMasterAdmin | IsMiniAdmin)
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ['get']
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class SingleUsersSpecificOrdersApiView(RetrieveAPIView):
    """
    Retrieve: get the information of a single order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser)
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ['get']
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user.id, is_paper=True)


# OrderFiles
class OrderFilesApiView(ListCreateAPIView):
    """
    GET: List all files for the orders by the user
    POST: create a new file
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsMasterAdmin)
    serializer_class = OrderFilesSerializer
    model = OrderFiles
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class OrderFilesDeleteApiView(RetrieveDestroyAPIView):
    """
    GET: List all files for the orders by the user
    DELETE: Delete order file
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsMasterAdmin)
    serializer_class = OrderFilesSerializer
    model = OrderFiles
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
