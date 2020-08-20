from django.test import TestCase
from mixer.backend.django import mixer
from authapp.models import Avatar, User


class AvatarModelTestcase(TestCase):
    """
    All Tests for the avatar model in tha authapp django application
    """

    @classmethod
    def setUpTestData(cls):
        """
        The data to be used in every test
        """
        cls.default = mixer.blend(User, username="joseph")
        cls.model = Avatar
        cls.model_data = mixer.blend(Avatar, user=cls.default, is_avatar=True, deletedAt=None)

    def test_meta_class_in_the_model(self):
        """
        Meta class test
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Avatar')
        self.assertEqual(meta.verbose_name, 'Avatar')
        self.assertEqual(meta.db_table, 'Avatar')
        self.assertEqual(meta.verbose_name_plural, 'Avatars')

    def test_no_of_fields_in_the_model(self):
        """
        Test the configured columns in the model
        """
        fields = list(self.model._meta.get_fields())
        self.assertEqual(len(fields), 8)

    def test_user_object_model_was_created(self):
        """
        Test user test data was created successfully
        """
        objects = User.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().__str__(), 'joseph')

    def test_delete_of_avatar_(self):
        """
        We can delete an avatar
        """
        objects = self.model.objects
        objects.first().delete()
        self.assertEqual(objects.count(), 0)

    def test_object_model_was_created(self):
        """
        Test data was created successfully
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().__str__(), 'joseph')

    def test_user_column_is_a_user_instance(self):
        """
        user column is a User Model instance
        """
        user = isinstance(self.model_data.user, User)
        self.assertTrue(user)

    def test_user_column_in_avatar_model(self):
        """
        Test the configured fields for the user column
        """
        user = self.model._meta.get_field(field_name='user')
        self.assertTrue(user)

    def test_avatar_column_in_avatar_model(self):
        """
        Test the configured fields for the user column
        """
        avatar = self.model._meta.get_field(field_name='avatar')
        self.assertTrue(avatar)

    def test_hidden_method(self):
        """
        Hides the avatar from user when they delete it
        """
        objects = self.model.objects.first()
        self.assertIsNone(objects.deletedAt)
        self.assertTrue(objects.is_avatar)
        objects.hidden()
        self.assertFalse(objects.is_avatar)
        self.assertIsNotNone(objects.deletedAt)
        self.assertEqual(self.model.objects.all().filter(is_avatar=True).count(), 0)
