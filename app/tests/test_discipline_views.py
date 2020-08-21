from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from app.views import (
    DeleteDisciplineAPIView, RetrieveDeletedDisciplineAPIView, RetrieveSpecificDisciplineAPIView,
    RetrieveTotalAllDisciplineAPIView, UpdateDisciplineAPIView,
    DisciplineCreateAPIView, RetrieveDisciplineAPIView, RetrieveAllActiveDisciplineAPIView)
from knox.models import AuthToken
from app.models import Discipline
from authapp.models import User
from django.conf import settings
from uuid import UUID


class DisciplineViewsAPIView(APITestCase):
    """
    Tests for all views related to the discipline model
    """

    def setUp(self) -> None:
        """
        All the data used in all tests
        """
        self.user = User.objects.create(uuid=UUID("475b1446-1d3e-4464-859c-bca080609041"), username="joseph",
                                        password="50391798", email="joseph@gmail.com", user_type="MASTER",
                                        is_staff=True, is_superuser=True)
        self.token = AuthToken.objects.create(user=self.user, expiry=settings.REST_KNOX['TOKEN_TTL'])
        self.api_Authentication()

    @classmethod
    def setUpTestData(cls):
        cls.current_app = "app"
        cls.admin_disciplines = reverse(viewname="app:discipline-specific-admin", current_app=cls.current_app)

    def api_Authentication(self):
        """
        Authorize the created user on the test_server
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token[1])

    def test_that_authenticated_master_admin_can_access_the_api(self):
        """
        Test that the authenticated user can retrieve data specific to them
        """
        response = self.client.get(resolve(self.admin_disciplines).route)
        print(response)
        # self.assertEqual(response.status_code, 404)
        # self.assertEqual(response.content_type, "text/html")

