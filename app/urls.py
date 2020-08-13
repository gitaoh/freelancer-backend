from django.urls import path
from .views import OrderApiView, UsersSpecificOrders, OrderDeleteApiView, SingleUsersSpecificOrdersApiView

app_name = "app"

urlpatterns = [
    path('orders/create', OrderApiView.as_view(), name="order-create"),
    path('orders', UsersSpecificOrders.as_view(), name="user-order"),
    path('orders/details/<uuid:uuid>', SingleUsersSpecificOrdersApiView.as_view(), name="single-user-order"),
    path('orders/delete/<uuid:uuid>', OrderDeleteApiView.as_view(), name="user-order"),
]
