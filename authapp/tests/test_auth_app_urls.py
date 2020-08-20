from django.test import TestCase
from django.urls import reverse, resolve
from authapp.views import (
    RegisterAPI, LoginAPI, AuthUserAPIView, UserUpdatePasswordApiView, UserDeleteApiView,
    RatingCreateAPIView)
from knox import views as knox_views


class AuthAppUrlsTestCase(TestCase):
    """
    Tests for auth app urls
    """

    @classmethod
    def setUpTestData(cls):
        """
        Testcase setupData
        Setup and tearDown on every test
        """
        cls.current_app = 'authapp'
        cls.register = reverse(viewname="authapp:register-auth-app", current_app=cls.current_app)
        cls.login = reverse(viewname='authapp:login', current_app=cls.current_app)
        cls.rating_create = reverse(viewname='authapp:rating-create', current_app=cls.current_app)
        cls.logout = reverse(viewname='authapp:logout', current_app=cls.current_app)
        cls.logout_all = reverse(viewname='authapp:logout-all', current_app=cls.current_app)
        cls.register_user = reverse(viewname="authapp:retrieve-user", current_app=cls.current_app)
        cls.delete_user = reverse(viewname="authapp:delete-user", current_app=cls.current_app,
                                  kwargs={"username": "username"})
        cls.update_user_password = reverse(viewname="authapp:update-user-password", current_app=cls.current_app,
                                           kwargs={"username": "username"})

    def app_name_namespace(self, response):
        """
        Test every api endpoint configured fields ie app_name, app_names, namespace
        """
        self.assertIn(response.app_name, response.app_names, msg="Auth app name has changed")
        self.assertEqual(response.namespace, response.app_name,
                         msg="Auth app name and its namespace are not the same ::=> should be.")
        self.assertIn(response.namespace, response.app_names, msg="Auth app namespace not in app_names ::=> should be.")

    def common_test_case_auth_app(self, test_name, route_name, route, url_name, view_class, kwargs=None, args=None):
        """
        Common test cases found in this testcase
        """
        response = resolve(route_name)
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = ()
        self.app_name_namespace(response)
        self.assertEqual(response.func.view_class, view_class)
        self.assertEqual(response.args, args, msg=f'Auth {test_name} api endpoint accepts arguments')
        self.assertEqual(response.kwargs, kwargs,
                         msg=f'Auth app {test_name} api endpoint accepts some keyword arguments')
        self.assertEqual(response.url_name, url_name, msg=f'Auth app {test_name} api endpoint name has changed')
        self.assertEqual(response.route, route)

    def test_register_api_endpoint(self):
        """
        Test the register api endpoint configured fields ie route, name, endpoint
        """
        self.common_test_case_auth_app(test_name="register", route_name=self.register, route='api/v1/auth/register',
                                       url_name="register-auth-app", view_class=RegisterAPI)

    def test_login_api_endpoint(self):
        """
        Test the login api endpoint configured fields ie route, name, endpoint
        """
        self.common_test_case_auth_app(test_name="login", route_name=self.login, route='api/v1/auth/login',
                                       url_name="login", view_class=LoginAPI)

    def test_logout_api_endpoint(self):
        """
        Test the logout api endpoint configured fields ie route, name, endpoint
        """
        self.common_test_case_auth_app(test_name="logout", route_name=self.logout, route='api/v1/auth/logout',
                                       url_name="logout", view_class=knox_views.LogoutView)

    def test_logout_all_api_endpoint(self):
        """
        Test the logout all api endpoint configured fields ie route, name, endpoint
        """
        self.common_test_case_auth_app(test_name="logout_all", route='api/v1/auth/logoutall',
                                       route_name=self.logout_all, url_name="logout-all",
                                       view_class=knox_views.LogoutAllView)

    def test_retrieve_user_api_endpoint(self):
        """
        Test the register user api endpoint configured fields ie route, name, endpoint
        """
        self.common_test_case_auth_app(test_name="retrieve user", route='api/v1/auth/user',
                                       route_name=self.register_user, url_name='retrieve-user',
                                       view_class=AuthUserAPIView)

    def test_update_user_password_api_endpoint(self):
        """
        Test the update user password api endpoint configured fields ie route, name, endpoint, kwargs
        """
        self.common_test_case_auth_app(test_name="update user password", url_name='update-user-password',
                                       route_name=self.update_user_password, view_class=UserUpdatePasswordApiView,
                                       route="api/v1/auth/users/password/reset/<str:username>",
                                       kwargs={"username": "username"})

    def test_delete_user_api_endpoint(self):
        """
        Test the delete user api endpoint configured fields ie route, name, endpoint, kwargs
        """
        self.common_test_case_auth_app(test_name="delete user", url_name='delete-user',
                                       route_name=self.delete_user, view_class=UserDeleteApiView,
                                       route="api/v1/auth/users/delete/<str:username>",
                                       kwargs={"username": "username"})

    def common_(self, view_name, func, url, url_name, app_name='authapp', args=None, kwargs=None):
        response = resolve(view_name)
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        self.assertEqual(response.args, args)
        self.assertEqual(response.app_name, app_name)
        self.assertIn(app_name, response.app_names)
        self.assertEqual(len(response.app_names), 1)
        self.assertEqual(response.namespace, app_name)
        self.assertIn(response.namespace, response.namespaces)
        self.assertEqual(response.route, url)
        self.assertEqual(response.func.view_class, func)
        self.assertEqual(response.url_name, url_name)
        self.assertEqual(response.kwargs, kwargs)

    def test_rating_create_url(self):
        """
        Create a rating for kromon
        """
        self.common_(view_name=self.rating_create, func=RatingCreateAPIView, url_name="rating-create",
                     url="api/v1/auth/rating/create")
