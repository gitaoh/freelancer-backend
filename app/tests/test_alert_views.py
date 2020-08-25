from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from app.views import (
    RetrieveAlertAPIView, AlertCreateAPIView, DeleteAlertAPIView, UpdateAlertAPIView,
    RetrieveInActiveAlertAPIView, RetrieveSingleAlertAPIView)
from authapp.models import User
from app.models import Alert
from uuid import UUID
from mixer.backend.django import mixer
from knox.models import AuthToken
from rest_framework import status


class AlertAPIViewsTestCase(APITestCase):
    """
    Tests for Views related to the Alert model
    """

    def setUp(self) -> None:
        self.uuid = UUID('217fe126-e175-11ea-87d0-0242ac130003')
        self.user = mixer.blend(User, is_superuser=True, is_staff=True, is_active=True, user_type='MASTER')
        self.alert = mixer.blend(Alert, deleted_by=None, is_active=True, title="Title 101", admin=self.user,
                                 uuid=self.uuid)
        self.token = AuthToken.objects.create(user=self.user)
        self.api_Authentication()

    def api_Authentication(self):
        """
        Authorize the created master on the test_server
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token[1])

    def test_alert_object_data_created(self):
        objects = Alert.objects.all()
        self.assertEqual(objects.count(), 1)
        objects = objects.first()
        self.assertIsInstance(objects.admin, User)
        self.assertTrue(objects.is_active)
        self.assertIsNone(objects.deleted_by)
        self.assertEqual(objects.__str__(), 'Title 101')

    def test_user_object_data_created(self):
        objects = User.objects.all()
        self.assertEqual(objects.count(), 1)
        objects = objects.first()
        self.assertEqual(objects.user_type, 'MASTER')
        self.assertTrue(objects.is_staff)
        self.assertTrue(objects.is_active)
        self.assertTrue(objects.is_superuser)

    def test_can_retrieve_created_alert_objects(self):
        response = self.client.get(reverse(viewname='app:alert-retrieve-active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
        self.assertEqual(response.request['PATH_INFO'], '/api/v1/admin/alert/retrieve/active')
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])
        self.assertEqual(response.resolver_match.func.view_class, RetrieveAlertAPIView)

    def test_cannot_retrieve_data(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse(viewname='app:alert-retrieve-active'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_alert_by_post(self):
        response = self.client.post(reverse('app:alert-create'), data={
            "title": "Title 202",
            "description": "Description of this alert"
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.common_(response, view=AlertCreateAPIView)

    def common_(self, response, view, url='/api/v1/admin/alert/create', method='POST'):
        self.assertEqual(response.resolver_match.func.view_class, view)
        self.assertEqual(response.request['PATCH_INFO'], url)
        self.assertEqual(response.request['CONTENT_TYPE'], 'application/json')
        self.assertEqual(response.request['REQUEST_METHOD'], method)
        self.assertIsNotNone(response.request['HTTP_AUTHORIZATION'])

    def test_description_is_required_to_create_alert(self):
        response = self.client.post(reverse('app:alert-create'), data={
            "title": "Title 202",
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.common_(response, view=AlertCreateAPIView)

    def test_title_is_required_to_create_alert(self):
        response = self.client.post(reverse('app:alert-create'), data={
            "description": "Description of this alert"
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.common_(response, view=AlertCreateAPIView)

    def test_from_is_required_to_create_alert(self):
        response = self.client.post(reverse('app:alert-create'), data={
            "title": "Title 202",
            "description": "Description of this alert",
            "to": ""
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.common_(response, view=AlertCreateAPIView)

    def test_to_is_required_to_create_alert(self):
        response = self.client.post(reverse('app:alert-create'), data={
            "title": "Title 202",
            "description": "Description of this alert",
            "to": ""
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.common_(response, view=AlertCreateAPIView)

    def test_title_unique_violation(self):
        response = self.client.post(reverse('app:alert-create'), data={
            "title": "Title 101",
            "description": "Description of this alert",
            "_from": "",
            "to": ""
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.common_(response, view=AlertCreateAPIView)

    def test_update_an_alert(self):
        response = self.client.patch(reverse('app:alert-update', kwargs={'uuid': self.uuid}), data={
            "title": "Title 102"
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.common_(response, url='/api/v1/admin/alert/update/<uuid:uuid>', method='PATCH', view=UpdateAlertAPIView)
        objects = Alert.objects.all().first().title
        self.assertEqual(objects, 'Title 102')

    def test_retrieve_active_alerts(self):
        response = self.client.get(reverse('app:alert-retrieve-active'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.common_(response, url='/api/v1/admin/alert/retrieve/active', method='GET', view=RetrieveAlertAPIView)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_deleted_alerts_(self):
        response = self.client.get(reverse('app:alert-retrieve-deleted'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.common_(response, url='/api/v1/admin/alert/retrieve/deleted', method='GET',
                     view=RetrieveInActiveAlertAPIView)
        self.assertEqual(len(response.data), 0)

    def test_delete_an_alert(self):
        response = self.client.delete(reverse('app:alert-delete', kwargs={'uuid': self.uuid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('app:alert-retrieve-deleted'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.common_(response, url='/api/v1/admin/alert/retrieve/deleted', method='GET',
                     view=RetrieveInActiveAlertAPIView)
        self.assertEqual(len(response.data), 1)
