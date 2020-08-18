from django.test import TestCase
from mixer.backend.django import mixer
from order.models import Notification
from app.models import MinimalModel
from authapp.models import User


class NotificationsModelTestCase(TestCase):
    """
    All tests for the Notification Model
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = Notification
        cls.default = 'joseph'
        cls.user = mixer.blend(User, usename=cls.default)
        cls.data = mixer.blend(cls.model, user=cls.user)

    def test_meta_class_properties(self):
        """
        Meta class model
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Notification')
        self.assertEqual(meta.verbose_name, 'Notification')
        self.assertEqual(meta.verbose_name_plural, 'Notifications')
        self.assertEqual(meta.db_table, 'Notification')

    def test_notification_objects_create(self):
        """
        Test test data was created successfully
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().__str__(), f"{self.user.username}, {objects.first().read}")

    def test_number_of_fields_in_models(self):
        """
        Allowed fields in the model
        """
        number = len(list(self.model._meta.get_fields()))
        self.assertEqual(number, 10)

    def test_can_delete_successfully(self):
        """
        Deletion Test
        """
        objects = self.model.objects
        objects.first().delete()
        self.assertEqual(objects.count(), 0)

    def test_can_update_successfully(self):
        """
        Update Test
        """
        objects = self.model.objects.first()
        objects.content = "New Notification"
        objects.save()
        self.assertEqual(objects.content, 'New Notification')

    def test_user_column(self):
        user = self.model._meta.get_field(field_name='user')
        self.assertEqual(user.default, None)
        self.assertIsNotNone(user.help_text)
        self.assertTrue(isinstance(self.model.objects.first().user, User))

    def test_is_sub_class_model(self):
        self.assertTrue(issubclass(Notification, MinimalModel))

    def test_content_column(self):
        """
        Test the content column in the model
        """
        content = self.model._meta.get_field(field_name='content')
        self.assertEqual(content.max_length, 10000)
        self.assertIsNotNone(content.help_text)

    def test_created_column(self):
        """
        Test the created column in the model
        """
        created = self.model._meta.get_field(field_name='created')
        self.assertEqual(created.default, None)
        self.assertIsNotNone(created.help_text)

    def test_notify_column(self):
        """
        Test the notify column in the model
        """
        notify = self.model._meta.get_field(field_name='notify')
        self.assertEqual(notify.max_length, 12)
        self.assertIsNotNone(notify.help_text)
        self.assertEqual(len(notify.choices), 3)

        for i in notify.choices:
            self.assertEqual(type(i), tuple)
            self.assertEqual(len(i), 2)

    def test_read_column(self):
        """
        Test the read column in the model
        """
        read = self.model._meta.get_field(field_name='read')
        self.assertFalse(read.default)
        self.assertIsNotNone(read.help_text)
