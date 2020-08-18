from uuid import UUID

from django.test import TestCase
from django.urls import resolve, reverse
from order.views import OrderApiView, UsersSpecificOrders, OrderDeleteApiView, SingleUsersSpecificOrdersApiView


class OrdersUrlsTestCase(TestCase):
    """
    All  Orders specific urls tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.current_app = "order"
        cls.order_create = reverse(viewname="order:create-order", current_app=cls.current_app)
        cls.users_order = reverse(viewname='order:users-order', current_app=cls.current_app)
        cls.single_user_order = reverse(viewname='order:single-user-order', current_app=cls.current_app,
                                        kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'})
        cls.delete_user_order = reverse(viewname='order:delete-user-order', current_app=cls.current_app,
                                        kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'})

    def app_name_namespace(self, response):
        self.assertEqual(response.namespace, self.current_app, msg='order namespace has changed.')
        self.assertEqual(response.app_name, self.current_app, msg='order name has changed.')
        self.assertIn(self.current_app, container=response.app_names,
                      msg='order names does not contain \'order\' has changed.')

    def test_single_user_order_url_endpoint(self):
        response = resolve(self.single_user_order)
        self.app_name_namespace(response=response)
        self.assertEqual(response.func.view_class, SingleUsersSpecificOrdersApiView,
                          msg="Route to Fetch a single order View has changed")
        self.assertEqual(response.url_name, 'single-user-order',
                         msg='Route name to Fetch a single order for the user has changed.')
        self.assertEqual(response.route, 'api/v1/orders/details/<uuid:uuid>',
                         msg='Route to fetch a single order data has changed.')
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')},
                         msg='Route to fetch a single users order does not accept kwargs does not accept'
                             ' any Keyword arguments.')
        self.assertEqual(response.args, (), msg='Route to fetch a single users order accepts any Key arguments.')

    def test_delete_user_order_url_endpoint(self):
        response = resolve(self.delete_user_order)
        self.app_name_namespace(response=response)
        self.assertEqual(response.func.view_class, OrderDeleteApiView,
                         msg="Route to delete a single order View has changed")
        self.assertEqual(response.url_name, 'delete-user-order',
                         msg='Route name to delete a single users orders has changed.')
        self.assertEqual(response.route, 'api/v1/orders/delete/<uuid:uuid>',
                         msg='Route to delete users orders has changed.')
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')},
                         msg='Route to delete users order does not accept kwargs does not accept any Keyword '
                             'arguments.')
        self.assertEqual(response.args, (), msg='Route to delete users orders accepts any Key arguments.')

    def test_order_create_url_endpoint(self):
        response = resolve(self.order_create)
        self.app_name_namespace(response=response)
        self.assertEquals(response.func.view_class, OrderApiView, msg='Route to create a new order View has changed')
        self.assertEqual(response.url_name, 'create-order', msg='Route name to create order has changed.')
        self.assertEqual(response.route, 'api/v1/orders/create', msg='Route to retrieve orders has changed.')
        self.assertEqual(response.kwargs, {}, msg='Route to create orders does not accept any Keyword arguments.')
        self.assertEqual(response.args, (), msg='Route to create orders accepts any Key arguments.')

    def test_user_order_url_endpoint(self):
        response = resolve(self.users_order)
        self.app_name_namespace(response=response)
        self.assertEquals(response.func.view_class, UsersSpecificOrders,
                          msg='Route to retrieve a all user orders has changed')
        self.assertEqual(response.url_name, 'users-order', msg='Route name to retrieve users orders has changed.')
        self.assertEqual(response.route, 'api/v1/orders/', msg='Route to retrieve orders has changed.')
        self.assertEqual(response.kwargs, {}, msg='Route to fetch users orders does not accept any Keyword arguments.')
        self.assertEqual(response.args, (), msg='Route to fetch users orders accepts any Key arguments.')
