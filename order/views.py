from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderFilesSerializer, CancelModeSerializer, MessageModelSerializer
from .models import Files, Order, Cancel, Writer, Message
from authapp.permissions.permissions import IsMiniAdmin, IsUser, IsMasterAdmin


class OrderApiView(CreateAPIView):
    """
    POST: Create a new order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsMasterAdmin)
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
    permission_classes = (IsAuthenticated, IsUser | IsMiniAdmin | IsMasterAdmin)
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
    permission_classes = (IsAuthenticated, IsMiniAdmin | IsMasterAdmin)
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


# Todo Update order to be Canceled


class OrderUpdateApiView(UpdateAPIView):
    """
    PUT: update order information
    PATCH: partial update to order information
    """
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["put", 'patch']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMasterAdmin)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user, is_paper=True, is_approved=False)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            var = request.data['writer']
            try:
                writer = Writer.objects.all().get(username__exact=var)
                self.perform_update_writer(writer, serializer)
            except Writer.DoesNotExist:
                return Response(
                    data={
                        "success": "Fail",
                        "error": "Writer does not exist",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    content_type='application/json',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except KeyError:
            self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update_writer(self, writer, serializer):
        serializer['writer'] = writer
        serializer.save()


class OrderCancelApiView(UpdateAPIView):
    """
    PUT: update order information
    PATCH: partial update to order information
    """
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["put", 'patch']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMasterAdmin)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user, is_paper=True, is_approved=False)

    def perform_update(self, serializer):
        serializer.cancel()


class OrderUnCancelApiView(UpdateAPIView):
    """
    PUT: update order information
    PATCH: partial update to order information
    """
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["put", 'patch']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMasterAdmin)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user, is_paper=True, is_approved=False)

    def perform_update(self, serializer):
        serializer.un_cancel()


class OrderApproveAPIView(UpdateAPIView):
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ['put', 'patch']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser | IsMasterAdmin)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user, is_paper=True, is_approved=False)

    def perform_update(self, serializer):
        serializer.approve()


class OrderDisApproveAPIView(UpdateAPIView):
    model = Order
    serializer_class = OrderSerializer
    http_method_names = ["put", 'patch']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user, is_paper=True, is_approved=True)

    def perform_update(self, serializer):
        serializer.un_approve()


class OrderDeleteApiView(DestroyAPIView):
    """
    Delete: delete an order
    """
    model = Order
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    http_method_names = ['delete']
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user, is_paper=True, deleted_by__isnull=True,
                                               deletedAt__isnull=True)

    def perform_destroy(self, instance):
        instance.deleted_by = self.request.user
        instance.save()
        instance.trash()


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


class OrderFileRetrieveListAPIView(ListAPIView):
    """
    Retrieve a list of files related to this order
    """
    model = Files
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser | IsMiniAdmin | IsMasterAdmin, IsAuthenticated)
    serializer_class = OrderFilesSerializer

    def get_queryset(self):
        return self.model.objects.all().filter(is_deleted=False, deletedAt__isnull=True)

    def get_object(self):
        # Todo relate to order
        return self.model.objects.all()


class OrderFileRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve a single order file
    """
    serializer_class = OrderFilesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser | IsMiniAdmin | IsMasterAdmin, IsAuthenticated)
    model = Files
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_object(self):
        return self.model.objects.all().filter(is_deleted=False, deletedAt__isnull=True)


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

[ X ] Create order
[ X ] Update order detail and files
[ X ] Approve order
[ X ] User specific order
[ X ] Single User specific order
[ X ] Delete an order
[ X ] List of all order - admin
[ X ] single order to admin - admin

[ X ] Canceled order should have a status='CANCELED' and should not be rendered

"""


# Todo check if order is already canceled in admin
class CreateCancelReasonAPIView(CreateAPIView):
    """
    Allow users to inform us of the reason they have to cancel an order
    """
    serializer_class = CancelModeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser | IsMasterAdmin, IsAuthenticated)
    model = Cancel
    http_method_names = ['post']

    def get_queryset(self):
        return self.model.objects.all()


class DeleteCancelReasonAPIView(DestroyAPIView):
    """
    Mark a reason as deleted
    """
    model = Cancel
    serializer_class = CancelModeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser | IsMasterAdmin, IsAuthenticated)
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True, deletedAt__isnull=True)

    def perform_destroy(self, instance):
        instance.trash()


class MessageCreateAPIView(CreateAPIView):
    """
    Create a message
    """
    model = Message
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser | IsMasterAdmin | IsMiniAdmin, IsAuthenticated)
    serializer_class = MessageModelSerializer

    def get_object(self):
        return self.model.objects.all()


class ListMessageAPIView(ListAPIView):
    """
    A list of all message of a order
    """
    serializer_class = MessageModelSerializer
    model = Message
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser | IsMasterAdmin | IsMiniAdmin, IsAuthenticated)

    def get_queryset(self):
        return self.model.objects.all().filter(is_notify=True, deletedAt__isnull=True)


class DeleteMessageAPIView(DestroyAPIView):
    """
    Delete a message
    """
    model = Message
    serializer_class = MessageModelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsMasterAdmin, IsAuthenticated)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(is_notify=True, deletedAt__isnull=True)
