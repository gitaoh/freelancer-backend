from authapp.views import RatingCreateAPIView, MakeAdminMasterAPIView
from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from rest_framework import status
from authapp.models import User, Rating
from knox.models import AuthToken
from uuid import UUID
from recycle.method_checker import MethodCheckerTestCase


class CreateRatingTestCase(MethodCheckerTestCase, APITestCase):
    model = Rating
    path = f"/{resolve(reverse('authapp:rating-create')).route}"
    POST = True

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(password='50391798', username="joseph", user_type="USER",
                                            email="joseph@gmail.com", uuid=UUID('475b1446-1d3e-4464-859c-bca080609041'))
        cls.view = reverse('authapp:rating-create')
        cls.token = AuthToken.objects.create(user=cls.user)

    def api_Authentication(self):
        """
        Authenticate a user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[1])

    def test_create_rating_view(self):
        self.api_Authentication()
        response = self.client.post(self.view, data={"rate": "1"}, content_type="application/json")
        print(response.data)
        self.assertEqual(response.resolver_match.func.view_class, RatingCreateAPIView)
        self.assertEqual(response.request['CONTENT_TYPE'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])


class MakeAdminMasterTestCase(APITestCase):
    path = f"/{resolve(reverse('authapp:make-user-master-admin', kwargs={'uuid': UUID('475b1446-1d3e-4464-859c-bca080609034')})).route}"
    view = MakeAdminMasterAPIView
    PATCH = True
    PUT = True

    @classmethod
    def setUpTestData(cls):
        cls.master = User.objects.create_user(password='50391798', username="joseph", user_type="MASTER",
                                              email="joseph@gmail.com",
                                              uuid=UUID('475b1446-1d3e-4464-859c-bca080609041'))
        cls.admin = User.objects.create_user(email="qwartypa@gmail.com", username="qwartypa", user_type="ADMIN",
                                             password="50391798", uuid=UUID('475b1446-1d3e-4464-859c-bca080609042'))
        cls.user = User.objects.create_user(password='50391798', username="user", user_type="USER",
                                            email="user@gmail.com", uuid=UUID('475b1446-1d3e-4464-859c-bca080609034'))
        cls.url_name = reverse('authapp:make-user-master-admin',
                               kwargs={"uuid": UUID('475b1446-1d3e-4464-859c-bca080609034')})
        cls.token = AuthToken.objects.create(user=cls.master)
        cls.token_user = AuthToken.objects.create(user=cls.user)
        cls.token_admin = AuthToken.objects.create(user=cls.admin)

    def api_Authentication(self):
        """
        Authenticate a user
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[1])

    # def test_delete_method_no_allowed(self):
    #     response = self.client.delete(self.view)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(response.request['PATH_INFO'], self.path)
    #     self.api_Authentication()
    #     response = self.client.delete(self.view)
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    #     self.assertEqual(response.request['REQUEST_METHOD'], 'DELETE')
    #     self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])
    #     self.assertEqual(response.request['PATH_INFO'], self.path)

    def test_test_object_create_(self):
        # Users
        objects = User.objects.all()
        self.assertEqual(objects.count(), 3)
        self.assertEqual(len(objects.filter(user_type='USER')), 1)
        self.assertEqual(len(objects.filter(user_type='ADMIN')), 1)
        self.assertEqual(len(objects.filter(user_type='MASTER')), 1)
        # AuthToken
        objects = AuthToken.objects.all()
        self.assertEqual(objects.count(), 3)

    # def test_can_retrieve_data_as_master_admin(self):
    #     self.api_Authentication()
    #     response = self.client.put(self.url_name)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.request['PATH_INFO'], self.path)
    #     self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
    #     self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])
    #     self.assertEqual(len(User.objects.all().filter(user_type='MASTER')), 2)

    def common_(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
        self.assertEqual(response.request['PATH_INFO'], self.path)

    def test_cannot_retrieve_data_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin[1])
        response = self.client.get(self.url_name)
        self.common_(response)

    def test_cannot_retrieve_data_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user[1])
        response = self.client.get(self.url_name)
        self.common_(response)
