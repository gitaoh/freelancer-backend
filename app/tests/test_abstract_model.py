from django.test import TestCase
from app.abstract import MinimalModel
from mixer.backend.django import mixer


class MinimalModelTestCase(TestCase):
    """
    All tests for this abstract models
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = MinimalModel

    def test_meta_class(self):
        """
        Test the class meta fields/columns
        """
        meta = self.model._meta
        self.assertTrue(meta.abstract)

    def test_number_of_fields_(self):
        """
        Allowed fields in the models
        """
        fields = list(self.model._meta.get_fields())
        self.assertEqual(len(fields), 4)

    def test_uuid_column(self):
        """
        UUID column test
        """
        uuid = self.model._meta.get_field(field_name='uuid')
        self.assertTrue(uuid.unique)
        self.assertFalse(uuid.null)
        self.assertFalse(uuid.blank)
        self.assertEqual(len(uuid.validators), 2)
        self.assertIsNotNone(uuid.help_text)
        self.assertEqual(uuid.max_length, 32)

    def test_created_at_column(self):
        """
        CreatedAt column test
        """
        created_at = self.model._meta.get_field(field_name='createdAt')
        self.assertTrue(created_at.auto_now_add)
        self.assertEqual(created_at.verbose_name, 'createdAt')

    def test_deleted_at_column(self):
        """
        DeletedAt column test
        """
        deleted_at = self.model._meta.get_field(field_name='deletedAt')
        self.assertTrue(deleted_at.null)
        self.assertEqual(deleted_at.verbose_name, 'deletedAt')

    def test_updated_at_column(self):
        """
        UpdatedAt column test
        """
        updated_at = self.model._meta.get_field(field_name='updatedAt')
        self.assertTrue(updated_at.auto_now)
        self.assertEqual(updated_at.verbose_name, 'updatedAt')
