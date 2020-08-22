from knox.auth import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveDestroyAPIView,
    ListCreateAPIView, RetrieveAPIView, )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import OrderSerializer, OrderFilesSerializer
from .models import Files, Order
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
        queryset = self.model.objects.all()
        return queryset


class UsersSpecificOrders(ListAPIView):
    """
    Get all User Specific Orders
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
    List: list of all orders
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
        return self.model.objects.all().filter(user=self.request.user, is_paper=True)


class OrderDeleteApiView(DestroyAPIView):
    """
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
        return self.model.objects.all().filter(user=self.request.user, is_paper=True)


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
        """
        Absolutely all orders
        """
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
        """
        User to view details of an order they have not deleted
        """
        return self.model.objects.all().filter(user=self.request.user, is_paper=True)


# OrderFiles
class OrderFilesApiView(CreateAPIView):
    """
    POST: create a new file
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsMasterAdmin)
    serializer_class = OrderFilesSerializer
    model = Files
    http_method_names = ['post']

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class OrderFilesDeleteApiView(DestroyAPIView):
    """
    DELETE: Delete order file
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsMasterAdmin)
    serializer_class = OrderFilesSerializer
    model = Files
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


"""

[ ] Create order
[ ] Update order detail and files
[ ] Approve order
[ ] User specific order
[ ] Single User specific order
[ ] Delete an order
[ ] List of all order - admin
[ ] single order to admin - admin

"""

"""

[ ] Canceled order should have a status='CANCELED' and should not be rendered

"""
