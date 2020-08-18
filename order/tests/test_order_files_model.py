from django.test import TestCase
from mixer.backend.django import mixer

from app.abstract import MinimalModel
from order.models import Files


class FilesModelTestCase(TestCase):
    """
    All tests for the Files model in the order application
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = Files
        cls.data = mixer.blend(Files, is_deleted=False)

    def test_meta_class_properties(self):
        """
        Meta class tests for the file models
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Files')
        self.assertEqual(meta.verbose_name, 'File')
        self.assertEqual(meta.verbose_name_plural, 'Files')
        self.assertEqual(meta.db_table, 'File')

    def test_number_of_fields_(self):
        """
        Number of Allowed fields
        """
        fields = len(list(self.model._meta.get_fields()))
        self.assertEqual(fields, 9)

    def test_is_subclass_of_(self):
        """
        Is a subclass of MinimalModel
        """
        self.assertTrue(issubclass(Files, MinimalModel))

    def test_object_was_created_successfully(self):
        """
        Object creation
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().__str__(), objects.first().description)

    def test_can_update_(self):
        """
        Object Updating
        """
        objects = self.model.objects.first()
        objects.is_deleted = True
        objects.save()
        self.assertTrue(objects.is_deleted)

    def test_can_delete_(self):
        """
        Object Updating
        """
        objects = self.model.objects.first()
        objects.deleted()
        self.assertTrue(objects.is_deleted)

    def test_can_restore_(self):
        """
        Object Restoration
        """
        objects = self.model.objects.first()
        # Delete
        objects.deleted()
        self.assertTrue(objects.is_deleted)
        self.assertEqual(self.model.objects.all().filter(is_deleted=False).count(), 0)
        # Restore
        objects.restore()
        self.assertFalse(objects.is_deleted)
        self.assertEqual(self.model.objects.all().filter(is_deleted=False).count(), 1)

    def test_description_column(self):
        """
        Discipline column Test
        """
        description = self.model._meta.get_field(field_name='description')
        self.assertTrue(description.blank)
        self.assertTrue(description.null)
        self.assertIsNotNone(description.help_text)
        self.assertEqual(description.max_length, 200)

    def test_file_column(self):
        """
        File column Test
        """
        file = self.model._meta.get_field(field_name='file')
        self.assertIsNotNone(file.help_text)

    def test_is_deleted_column(self):
        """
        is_deleted column Test
        """
        is_deleted = self.model._meta.get_field(field_name='is_deleted')
        self.assertIsNotNone(is_deleted.help_text)
        self.assertFalse(is_deleted.default)
