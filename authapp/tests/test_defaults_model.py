from django.test import TestCase
from mixer.backend.django import mixer
from authapp.models import Defaults, User, Writer, MinimalModel


class DefaultModelTestCase(TestCase):
    """
    All tests for Default Model in the authapp django application
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = Defaults
        cls.user = mixer.blend(User, username='joseph')
        cls.writer = mixer.blend(Writer, username='joseph')
        cls.model_data = mixer.blend(cls.model, user=cls.user, writer=cls.writer, native=True)

    def test_meta_class(self):
        """
        Test the configured meta class
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Defaults')
        self.assertEqual(meta.verbose_name, 'Default')
        self.assertEqual(meta.verbose_name_plural, 'Defaults')
        self.assertEqual(meta.db_table, 'Default')

    def test_number_of_fields_(self):
        """
        Total number of fields configured
        """
        default = list(self.model._meta.get_fields())
        self.assertEqual(len(default), 12)

    def test_default_object_created(self):
        """
        Test that a single default object was created
        """
        default = self.model.objects
        self.assertEqual(default.all().count(), 1)
        self.assertEqual(default.first().__str__(), f'{self.user.username} -> {self.writer.username}')

    def test_user_column_is_user_instance(self):
        """
        Test that default user is a User object
        """
        user = self.model.objects.first()
        self.assertTrue(isinstance(user.user, User))

    def test_writer_column_is_user_instance(self):
        """
        Test that default writer is a Writer object
        """
        writer = self.model.objects.first()
        self.assertTrue(isinstance(writer.writer, Writer))

    def test_user_is_a_subclass(self):
        """
        Is Subclass of MinimaModel
        """
        self.assertTrue(issubclass(Defaults, MinimalModel))

    def test_can_delete_created_data_object(self):
        """
        Deleting an object successfully
        """
        objects = self.model.objects
        objects.first().delete()
        self.assertEqual(objects.count(), 0)

    def test_can_update_created_data_object(self):
        """
        Update an object successfully
        """
        objects = self.model.objects.first()
        objects.native = False
        objects.save()
        self.assertFalse(objects.native)

    def topic_paper_format_(self, name):
        field = self.model._meta.get_field(field_name=name)
        self.assertTrue(field.null)
        self.assertEqual(field.max_length, 200)
        self.assertIsNotNone(field.help_text)

    def test_format_column(self):
        """
        Test the format column
        """
        self.topic_paper_format_('format')

    def test_native_column(self):
        """
        Test the native column
        """
        native = self.model._meta.get_field(field_name='native')
        self.assertIsNotNone(native.help_text)

    def test_paper_column(self):
        """
        Test the paper column
        """
        self.topic_paper_format_('paper')

    def test_topic_column(self):
        """
        Test the topic column
        """
        self.topic_paper_format_('topic')

    def test_academic_column(self):
        """
        Test the topic column
        """
        academic = self.model._meta.get_field('academic')
        self.assertEqual(academic.max_length, 17)
        self.assertIsNotNone(academic.help_text)
        self.assertIsNone(academic.default)
        self.assertEqual(len(academic.choices), 6)
        self.assertTrue(academic.null)

        for i in academic.choices:
            self.assertEqual(len(i), 2)
            self.assertEqual(type(i), tuple)

    def test_user_column(self):
        """
        Test the user column
        """
        user = self.model._meta.get_field(field_name='user')
        self.assertIsNone(user.default)

    def test_writer_column(self):
        """
        Test the writer column
        """
        writer = self.model._meta.get_field(field_name='writer')
        self.assertIsNone(writer.default)
