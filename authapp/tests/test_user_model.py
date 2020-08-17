from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from mixer.backend.django import mixer

from app.abstract import MinimalModel
from authapp.models import User


class UserModelTestCase(TestCase):
    """
    All tests for the User Model in the django application
    """

    @classmethod
    def setUpTestData(cls):
        """
        Testing data
        """
        cls.model = User
        cls.default = 'joseph'
        cls.model_data = mixer.blend(cls.model, username=cls.default)

    def test_meta_class(self):
        """
        Test the meta class for the model
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'User')
        self.assertEqual(meta.verbose_name, 'User')
        self.assertEqual(meta.verbose_name_plural, 'Users')
        self.assertEqual(meta.db_table, 'User')

    def test_number_of_fields(self):
        """
        Test the total number of fields defined in the model
        """
        number = list(self.model._meta.get_fields())
        self.assertEqual(len(number), 30)

    def test_is_subclass(self):
        """
        User model should be a subclass of MinimalModel and AbstractUser
        """
        self.assertTrue(issubclass(User, MinimalModel))
        self.assertTrue(issubclass(User, AbstractUser))

    def test_user_model_test_data_was_created_successfully(self):
        """
        Test that a data was created successfully
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertTrue(isinstance(objects.first(), User))
        self.assertEqual(objects.first().__str__(), self.default)

    def test_can_delete_user(self):
        """
        Deleting a user
        """
        user = self.model.objects
        user.first().delete()
        self.assertEqual(user.count(), 0)

    def test_can_update_user(self):
        """
        Updating a user
        """
        user = self.model.objects.first()
        user.username = 'Noemi'
        user.save()
        self.assertEqual(user.username, 'Noemi')

    def test_phone_number_column(self):
        """
        Test the Phone number column config
        """
        phone = self.model._meta.get_field(field_name='phone_number')
        self.assertTrue(phone.null)
        self.assertTrue(phone.blank)
        self.assertTrue(phone.unique)
        self.assertIsNotNone(phone.help_text)
        self.assertEqual(len(phone.validators), 3)

    def test_updates_column(self):
        """
        Test the updates column config
        """
        updates = self.model._meta.get_field(field_name='updates')
        self.assertTrue(updates.default)
        self.assertIsNotNone(updates.help_text)
        self.assertEqual(updates.verbose_name, 'updates')

    def test_user_type_column(self):
        """
        Test the user type column config
        """
        user_type = self.model._meta.get_field(field_name='user_type')
        self.assertEqual(user_type.choices[1][0], user_type.default)
        self.assertIsNotNone(user_type.help_text)
        self.assertEqual(user_type.verbose_name, 'type')
        self.assertEqual(user_type.max_length, 6)

        for i in user_type.choices:
            self.assertEqual(len(i), 2)
            self.assertEqual(type(i), tuple)

    def test_terms_column(self):
        """
        Test the terms column config
        """
        terms = self.model._meta.get_field(field_name='terms')
        self.assertTrue(terms.default)
        self.assertEqual(terms.verbose_name, 'terms')
        self.assertIsNotNone(terms.help_text)

    def test_email_column(self):
        """
        Test the terms column config
        """
        email = self.model._meta.get_field(field_name='email')
        self.assertEqual(email.verbose_name, 'email')
        self.assertEqual(email.max_length, 254)
        self.assertFalse(email.null)
        self.assertFalse(email.blank)
        self.assertTrue(email.unique)
        self.assertEqual(len(email.validators), 3)
