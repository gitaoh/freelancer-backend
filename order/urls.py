from django.urls import path
from .views import OrderApiView, UsersSpecificOrders, OrderDeleteApiView, SingleUsersSpecificOrdersApiView

app_name = "order"

urlpatterns = [
    # Create order posted by user
    path('create', OrderApiView.as_view(), name="create-order"),
    # Fetch orders for the user
    path('', UsersSpecificOrders.as_view(), name="users-order"),
    # Fetch a single order for the user
    path('details/<uuid:uuid>', SingleUsersSpecificOrdersApiView.as_view(), name="single-user-order"),
    # Delete a single order fo the user
    path('delete/<uuid:uuid>', OrderDeleteApiView.as_view(), name="delete-user-order"),
]
