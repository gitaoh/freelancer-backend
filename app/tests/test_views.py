from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from app.views import (
    DeleteDisciplineAPIView, RetrieveDeletedDisciplineAPIView, RetrieveSpecificDisciplineAPIView,
    RetrieveTotalAllDisciplineAPIView, UpdateDisciplineAPIView,
    DisciplineCreateAPIView, RetrieveDisciplineAPIView, RetrieveAllActiveDisciplineAPIView,
    RetrieveSpecificPaperTypeAPIView)
from knox.models import AuthToken
from app.models import Discipline, PaperType
from authapp.models import User
from django.conf import settings
from uuid import UUID
from django.utils.timezone import now


class CommonTestCase(APITestCase):
    """
    Common tests in a view
    """
    route = None
    method = None
    model = Discipline
    absolute_route = None
    view = None
    not_allowed = []

    def setUp(self) -> None:
        """
        All the data used in all tests
        """
        self.user = User.objects.create(uuid=UUID("475b1446-1d3e-4464-859c-bca080609041"), username="user",
                                        password="50391798", email="user@gmail.com", user_type="USER",
                                        is_staff=False, is_superuser=False)
        self.admin = User.objects.create(uuid=UUID("475b1446-1d3e-4464-859c-bca080609042"), username="admin",
                                         password="50391798", email="admin@gmail.com", user_type="ADMIN",
                                         is_staff=True, is_superuser=True)
        self.master = User.objects.create(uuid=UUID("475b1446-1d3e-4464-859c-bca080609043"), username="joseph",
                                          password="50391798", email="joseph@gmail.com", user_type="MASTER",
                                          is_staff=True, is_superuser=True)
        self.token = AuthToken.objects.create(user=self.master, expiry=settings.REST_KNOX['TOKEN_TTL'])
        self.admin_token = AuthToken.objects.create(user=self.admin, expiry=settings.REST_KNOX['TOKEN_TTL'])
        self.user_token = AuthToken.objects.create(user=self.user, expiry=settings.REST_KNOX['TOKEN_TTL'])
        self.discipline = self.model.objects.create(uuid=UUID("475b1446-1d3e-4464-859c-bca080609041"),
                                                    admin=self.master, name="discipline 101",
                                                    description="The description of discipline 101")
        self.discipline_deleted = self.model.objects.create(uuid=UUID("475b1446-1d3e-4464-859c-bca080609042"),
                                                            admin=self.master, name="discipline 102", is_active=False,
                                                            deletedAt=now(),
                                                            description="The description of discipline 102")
        self.api_Authentication()

    def api_Authentication(self):
        """
        Authorize the created master on the test_server
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token[1])

    def user_api_Authentication(self):
        """
        Authorize the created user on the test_server
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token[1])

    def admin_api_Authentication(self):
        """
        Authorize the created admin on the test_server
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token[1])

    def test_user_objects_created(self):
        objects = User.objects.all()
        self.assertTrue(
            objects.get(username="user", password="50391798", email="user@gmail.com", user_type="USER", is_staff=False,
                        is_superuser=False))
        self.assertTrue(
            objects.get(username="admin", password="50391798", email="admin@gmail.com", user_type="ADMIN",
                        is_staff=True, is_superuser=True))
        self.assertTrue(
            objects.get(username="joseph", password="50391798", email="joseph@gmail.com", user_type="MASTER",
                        is_staff=True, is_superuser=True))
        self.assertEqual(len(objects.filter(user_type="MASTER")), 1)
        self.assertEqual(len(objects.filter(user_type="ADMIN")), 1)
        self.assertEqual(len(objects.filter(user_type="USER")), 1)

    def not_allowed_test(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNotNone(response.data["detail"])
        self.assertEqual(response.status_text, "Unauthorized")

    def tes_not_allowed_methods(self):
        if self.assertIn(container=self.not_allowed, member='GET'):
            print(self.not_allowed)
            response = self.client.get(self.absolute_route)
            self.not_allowed_test(response)
        elif self.assertIn(container=self.not_allowed, member='POST'):
            print(self.not_allowed)
            response = self.client.post(self.absolute_route, data={})
            self.not_allowed_test(response)
        elif self.assertIn(container=self.not_allowed, member='PUT'):
            print(self.not_allowed)
            response = self.client.put(self.absolute_route, data={})
            self.not_allowed_test(response)
        elif self.assertIn(container=self.not_allowed, member='PATCH'):
            print(self.not_allowed)
            response = self.client.patch(self.absolute_route, data={})
            self.not_allowed_test(response)
        elif self.assertIn(container=self.not_allowed, member='DELETE'):
            print(self.not_allowed)
            response = self.client.delete(self.absolute_route, data={})
            self.not_allowed_test(response)
        else:
            return

    def path_info_method_query(self, response, query=''):
        self.assertEqual(response.request['PATH_INFO'], self.route)
        self.assertEqual(response.request['REQUEST_METHOD'], self.method)
        self.assertEqual(response.request['CONTENT_TYPE'], 'application/octet-stream')
        self.assertEqual(response.request["QUERY_STRING"], query)
        self.assertEqual(len(response.templates), 0)
        self.assertIsNone(response.template_name)

    def test_model_objects_created(self):
        objects = self.model.objects.all()
        self.assertEqual(objects.count(), 2)
        self.assertEqual(len(objects.filter(is_active=True, deletedAt__isnull=True)), 1)
        self.assertEqual(len(objects.filter(is_active=True)), 1)

    def test_user_will_no_be_able_to_get_data(self):
        # Authenticate as a user
        self.user_api_Authentication()
        response = self.client.get(self.absolute_route, content_type="application/octet-stream")
        self.path_info_method_query(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(response.data["detail"])
        self.assertEqual(response.resolver_match.func.view_class, self.view)
        self.assertEqual(response.status_text, "Forbidden")
        self.assertEqual(response.data["detail"], 'You do not have permission to perform this action.')

    def test_admin_will_no_be_able_to_get_data(self):
        # Authenticate as a admin
        self.admin_api_Authentication()
        response = self.client.get(self.absolute_route, content_type="application/octet-stream")
        self.path_info_method_query(response)
        self.assertIsNotNone(response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_text, "Forbidden")
        self.assertEqual(response.resolver_match.func.view_class, self.view)
        self.assertEqual(response.data["detail"], 'You do not have permission to perform this action.')

    def test_cannot_authorise_unauthenticated_user_not_to_view_data(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.absolute_route, content_type="application/octet-stream")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNotNone(response.data["detail"])
        self.assertEqual(response.status_text, "Unauthorized")
        self.assertIsNone(response.template_name)
        self.assertEqual(len(response.templates), 0)
        self.assertEqual(response.resolver_match.func.view_class, self.view)
        self.assertEqual(response.data["detail"], 'Authentication credentials were not provided.')


class RetrieveSpecificViewsTestCase(CommonTestCase):
    absolute_route = reverse(viewname="app:discipline-specific-admin", current_app='app')
    route = f"/{resolve(absolute_route).route}"
    method = "GET"
    view = RetrieveSpecificDisciplineAPIView
    not_allowed = ['DELETE', 'PATCH', 'PUT', 'POST']

    def test_that_authenticated_master_admin_can_access_the_api(self):
        """
        Test that the authenticated user can retrieve data specific to them
        """
        self.api_Authentication()
        response = self.client.get(self.absolute_route, content_type="application/octet-stream")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.discipline.name)
        self.assertEqual(response.data[0]["description"], self.discipline.description)
        self.path_info_method_query(response)


class RetrieveSpecificPaperTypeAPIViewTestCase(RetrieveSpecificViewsTestCase):
    absolute_route = reverse(viewname="app:paper-type-specific-admin", current_app='app')
    route = f"/{resolve(absolute_route).route}"
    view = RetrieveSpecificPaperTypeAPIView
    model = PaperType

# class RetrieveAllActiveDisciplineTestCase(CommonTestCase)
