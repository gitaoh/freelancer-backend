from django.urls import path, include
from .views import (
    OrderApiView, UsersSpecificOrders, OrderDeleteApiView, SingleUsersSpecificOrdersApiView,
    SingleTOAdminsOrderApiView, OrderCancelApiView, OrderUnCancelApiView, OrderApproveAPIView, OrderDisApproveAPIView,
    CreateCancelReasonAPIView, DeleteCancelReasonAPIView, OrderFilesApiView, OrderFileRetrieveAPIView,
    OrderFileRetrieveListAPIView, OrderFilesDeleteApiView, OrderUpdateApiView, MessageCreateAPIView, ListMessageAPIView,
    DeleteMessageAPIView)

app_name = "order"

urlpatterns = [
    path('create', OrderApiView.as_view(), name="create-order"),
    path('', UsersSpecificOrders.as_view(), name="users-order"),
    path('details/<uuid:uuid>', SingleUsersSpecificOrdersApiView.as_view(), name="single-user-order"),
    path('update/<uuid:uuid>', OrderUpdateApiView.as_view(), name="order-update"),
    path('delete/<uuid:uuid>', OrderDeleteApiView.as_view(), name="delete-user-order"),
    path('admin/', include([
        path('single/<uuid:uuid>', SingleTOAdminsOrderApiView.as_view(), name="admin-single")
    ])),
    path('files/', include([
        path('create', OrderFilesApiView.as_view(), name='files-create'),
        path('retrieve/<uuid:uuid>', OrderFileRetrieveAPIView.as_view(), name="file-retrieve"),
        path('retrieve/list', OrderFileRetrieveListAPIView.as_view(), name="file-retrieve"),
        path('delete/<uuid:uuid>', OrderFilesDeleteApiView.as_view(), name='files-delete')
    ])),
    # Before approving on frontend put up some checks for the user to verify
    path('approve/<uuid:uuid>', OrderApproveAPIView.as_view(), name="order-approve"),
    path('disapprove/<uuid:uuid>', OrderDisApproveAPIView.as_view(), name="order-dis-approve"),
    path('cancel/<uuid:uuid>', OrderCancelApiView.as_view(), name="order-cancel"),
    path('uncancel/<uuid:uuid>', OrderUnCancelApiView.as_view(), name="order-un-cancel"),
    path('cancel/', include([
        path('create', CreateCancelReasonAPIView.as_view(), name="cancel-create"),
        path('delete/<uuid:uuid>', DeleteCancelReasonAPIView.as_view(), name="cancel-delete")
    ])),
    path('message/', include([
        path('create', MessageCreateAPIView.as_view(), name="message-create"),
        path('retrieve/all', ListMessageAPIView.as_view(), name="message-list"),
        path('delete/<uuid:uuid>', DeleteMessageAPIView.as_view(), name="message-delete")
    ])),
]
