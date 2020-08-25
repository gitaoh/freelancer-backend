from django.urls import path, include
from .views import OrderApiView, UsersSpecificOrders, OrderDeleteApiView, SingleUsersSpecificOrdersApiView, \
    SingleTOAdminsOrderApiView, OrderCancelApiView, OrderUnCancelApiView, OrderApproveAPIView, OrderDisApproveAPIView, \
    CreateCancelReasonAPIView, DeleteCancelReasonAPIView

app_name = "order"

urlpatterns = [
    path('create', OrderApiView.as_view(), name="create-order"),
    path('', UsersSpecificOrders.as_view(), name="users-order"),
    path('details/<uuid:uuid>', SingleUsersSpecificOrdersApiView.as_view(), name="single-user-order"),
    path('delete/<uuid:uuid>', OrderDeleteApiView.as_view(), name="delete-user-order"),
    path('admin/', include([
        path('single/<uuid:uuid>', SingleTOAdminsOrderApiView.as_view(), name="admin-single")
    ])),
    # Before approving on frontend put up some checks for the user to verify
    path('approve/<uuid:uuid>', OrderApproveAPIView.as_view(), name="order-approve"),
    path('disapprove/<uuid:uuid>', OrderDisApproveAPIView.as_view(), name="order-dis-approve"),
    path('cancel/<uuid:uuid>', OrderCancelApiView.as_view(), name="order-cancel"),
    path('uncancel/<uuid:uuid>', OrderUnCancelApiView.as_view(), name="order-un-cancel"),
    path('cancel/', include([
        path('create', CreateCancelReasonAPIView.as_view(), name="cancel-create"),
        path('delete/<uuid:uuid>', DeleteCancelReasonAPIView.as_view(), name="cancel-delete")
    ]))
]
