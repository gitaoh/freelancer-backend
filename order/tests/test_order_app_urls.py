from uuid import UUID

from django.test import TestCase
from django.urls import resolve, reverse
from order.views import (
    OrderApiView, UsersSpecificOrders, OrderDeleteApiView, SingleUsersSpecificOrdersApiView,
    OrderDisApproveAPIView, OrderApproveAPIView, OrderUnCancelApiView, OrderCancelApiView, SingleTOAdminsOrderApiView,
    CreateCancelReasonAPIView, DeleteCancelReasonAPIView)


class OrdersUrlsTestCase(TestCase):
    """
    All  Orders specific urls tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.current_app = "order"
        cls.order_create = reverse(viewname="order:create-order", current_app=cls.current_app)
        cls.users_order = reverse(viewname='order:users-order', current_app=cls.current_app)
        cls.cancel_create = reverse(viewname='order:cancel-create', current_app=cls.current_app)
        cls.single_user_order = reverse(viewname='order:single-user-order', current_app=cls.current_app,
                                        kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'})
        cls.delete_user_order = reverse(viewname='order:delete-user-order', current_app=cls.current_app,
                                        kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'})
        cls.admin_single = reverse('order:admin-single', kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'},
                                   current_app=cls.current_app)
        cls.order_cancel = reverse('order:order-cancel', kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'},
                                   current_app=cls.current_app)
        cls.order_un_cancel = reverse('order:order-un-cancel', kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'},
                                      current_app=cls.current_app)
        cls.order_approve = reverse('order:order-approve', kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'},
                                    current_app=cls.current_app)
        cls.order_dis_approve = reverse('order:order-dis-approve',
                                        kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'},
                                        current_app=cls.current_app)
        cls.cancel_delete = reverse('order:cancel-delete',
                                    kwargs={"uuid": 'deab7f06-de61-11ea-87d0-0242ac130003'},
                                    current_app=cls.current_app)

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
        self.assertEqual(response.func.view_class, OrderApiView, msg='Route to create a new order View has changed')
        self.assertEqual(response.url_name, 'create-order', msg='Route name to create order has changed.')
        self.assertEqual(response.route, 'api/v1/orders/create', msg='Route to retrieve orders has changed.')
        self.assertEqual(response.kwargs, {}, msg='Route to create orders does not accept any Keyword arguments.')
        self.assertEqual(response.args, (), msg='Route to create orders accepts any Key arguments.')

    def test_user_order_url_endpoint(self):
        response = resolve(self.users_order)
        self.app_name_namespace(response=response)
        self.assertEqual(response.func.view_class, UsersSpecificOrders,
                         msg='Route to retrieve a all user orders has changed')
        self.assertEqual(response.url_name, 'users-order', msg='Route name to retrieve users orders has changed.')
        self.assertEqual(response.route, 'api/v1/orders/', msg='Route to retrieve orders has changed.')
        self.assertEqual(response.kwargs, {}, msg='Route to fetch users orders does not accept any Keyword arguments.')
        self.assertEqual(response.args, (), msg='Route to fetch users orders accepts any Key arguments.')

    def test_admin_single_url_endpoint(self):
        response = resolve(self.admin_single)
        self.assertEqual(response.route, 'api/v1/orders/admin/single/<uuid:uuid>')
        self.assertEqual(response.args, ())
        self.assertEqual(response.func.view_class, SingleTOAdminsOrderApiView)
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')})
        self.app_name_namespace(response)
        self.assertEqual(response.url_name, 'admin-single')

    def test_order_cancel_url_endpoint(self):
        response = resolve(self.order_cancel)
        self.assertEqual(response.route, 'api/v1/orders/cancel/<uuid:uuid>')
        self.assertEqual(response.args, ())
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')})
        self.app_name_namespace(response)
        self.assertEqual(response.func.view_class, OrderCancelApiView)
        self.assertEqual(response.url_name, 'order-cancel')

    def test_order_un_cancel_url_endpoint(self):
        response = resolve(self.order_un_cancel)
        self.assertEqual(response.route, 'api/v1/orders/uncancel/<uuid:uuid>')
        self.assertEqual(response.args, ())
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')})
        self.app_name_namespace(response)
        self.assertEqual(response.func.view_class, OrderUnCancelApiView)
        self.assertEqual(response.url_name, 'order-un-cancel')

    def test_order_dis_approve_url_endpoint(self):
        response = resolve(self.order_dis_approve)
        self.assertEqual(response.route, 'api/v1/orders/disapprove/<uuid:uuid>')
        self.assertEqual(response.args, ())
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')})
        self.app_name_namespace(response)
        self.assertEqual(response.func.view_class, OrderDisApproveAPIView)
        self.assertEqual(response.url_name, 'order-dis-approve')

    def test_order_approve_url_endpoint(self):
        response = resolve(self.order_approve)
        self.assertEqual(response.route, 'api/v1/orders/approve/<uuid:uuid>')
        self.assertEqual(response.args, ())
        self.assertEqual(response.func.view_class, OrderApproveAPIView)
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')})
        self.app_name_namespace(response)
        self.assertEqual(response.url_name, 'order-approve')

    def test_cancel_create_url_endpoint(self):
        response = resolve(self.cancel_create)
        self.assertEqual(response.route, 'api/v1/orders/cancel/create')
        self.assertEqual(response.args, ())
        self.assertEqual(response.kwargs, {})
        self.assertEqual(response.func.view_class, CreateCancelReasonAPIView)
        self.assertEqual(response.url_name, 'cancel-create')
        self.app_name_namespace(response)

    def test_cancel_delete_url_endpoint(self):
        response = resolve(self.cancel_delete)
        self.assertEqual(response.kwargs, {"uuid": UUID('deab7f06-de61-11ea-87d0-0242ac130003')})
        self.assertEqual(response.args, ())
        self.assertEqual(response.route, 'api/v1/orders/cancel/delete/<uuid:uuid>')
        self.app_name_namespace(response)
        self.assertEqual(response.func.view_class, DeleteCancelReasonAPIView)
