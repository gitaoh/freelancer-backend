from rest_framework import status
from rest_framework.test import APITestCase
from uuid import UUID
from authapp.models import User
from knox.models import AuthToken


class MethodCheckerTestCase:
    """
    Check/verify Methods allowed in a view
    """
    # View to tests
    view = None
    # url path to perform requests to
    path = None
    # GET request allowed in this route
    GET = False
    # DELETE request allowed in this route
    DELETE = False
    # PATCH request allowed in this route
    PATCH = False
    # PUT request allowed in this route
    PUT = False
    # POST request allowed in this route
    POST = False

    # @classmethod
    # def setUpTestData(cls):
    #     cls.master = User.objects.create_user(password='50391798', username="joseph", user_type="MASTER",
    #                                           email="joseph@gmail.com",
    #                                           uuid=UUID('475b1446-1d3e-4464-859c-bca080609041'))
    #     cls.token = AuthToken.objects.create(user=cls.master)

    def api_Authentication(self):
        """
        No Authentication
        """
        pass
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token[1])

    def test_get_method_no_allowed(self):
        if self.GET:
            return False
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.api_Authentication()
        response = self.client.get(self.view)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.request['CONTENT_TYPE'], 'application/octet-stream')
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])
        self.assertEqual(response.request['PATH_INFO'], self.path)

    def test_delete_method_no_allowed(self):
        if self.DELETE:
            return False
        response = self.client.delete(self.view)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.api_Authentication()
        response = self.client.delete(self.view)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.request['REQUEST_METHOD'], 'DELETE')
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])
        self.assertEqual(response.request['PATH_INFO'], self.path)

    def test_put_method_no_allowed(self):
        if self.PUT:
            return False
        response = self.client.put(self.view)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.api_Authentication()
        response = self.client.put(self.view)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.request['REQUEST_METHOD'], 'PUT')
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])

    def test_patch_method_no_allowed(self):
        if self.PATCH:
            return False
        response = self.client.patch(self.view)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.api_Authentication()
        response = self.client.patch(self.view)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.assertEqual(response.request['REQUEST_METHOD'], 'PATCH')
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])

    def test_post_method_no_allowed(self):
        if self.POST:
            return False
        response = self.client.post(self.view, data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.api_Authentication()
        response = self.client.patch(self.view)
        self.assertEqual(response.request['PATH_INFO'], self.path)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')
