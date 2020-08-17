from django.test import TestCase
from mixer.backend.django import mixer
from order.models import Writer, MinimalModel


class WriterModelTestCase(TestCase):
    """
    All tests  for the writer model in the order django application
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = Writer
        cls.default = {'username': 'qwartypa', 'first_name': 'joseph', 'last_name': 'gitau'}
        cls.data = mixer.blend(Writer, is_active=True, username=cls.default['username'],
                               first_name=cls.default['first_name'],
                               last_name=cls.default['last_name'])

    def test_meta_class_properties(self):
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Writer')
        self.assertEqual(meta.verbose_name, 'Writer')
        self.assertEqual(meta.verbose_name_plural, 'Writers')
        self.assertEqual(meta.db_table, 'Writer')

    def test_number_of_fields_(self):
        fields = len(list(self.model._meta.get_fields()))
        self.assertEqual(fields, 13)

    def test_models_created_(self):
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().__str__(), objects.first().username)

    def test_can_delete_(self):
        objects = self.model.objects.first()
        objects.deactivate()
        self.assertFalse(objects.is_active)

    def test_can_restore_(self):
        objects = self.model.objects.first()
        objects.is_active = False
        objects.activate()
        self.assertTrue(objects.is_active)

    def test_is_subclass_(self):
        self.assertTrue(issubclass(Writer, MinimalModel))

    def test_username_column(self):
        username = self.model._meta.get_field(field_name='username')
        self.assertTrue(username.unique)
        self.assertEqual(username.verbose_name, 'username')
        self.assertEqual(username.max_length, 150)
        self.assertEqual(len(username.validators), 2)
        self.assertIsNotNone(username.help_text)
        self.assertIsNotNone(username.error_messages)

    def test_first_name_col_(self):
        field = self.model._meta.get_field('first_name')
        self.assertEqual(field.verbose_name, 'first name')
        self.assertEqual(field.max_length, 30)
        self.assertTrue(field.blank)
        self.assertIsNotNone(field.help_text)

    def test_last_name_col_(self):
        field = self.model._meta.get_field('last_name')
        self.assertEqual(field.verbose_name, 'last name')
        self.assertEqual(field.max_length, 150)
        self.assertTrue(field.blank)
        self.assertIsNotNone(field.help_text)

    def test_email_address_col_(self):
        field = self.model._meta.get_field('email')
        self.assertEqual(field.verbose_name, 'email address')
        self.assertTrue(field.unique)
        self.assertEqual(field.max_length, 254)
        self.assertFalse(field.blank)
        self.assertIsNotNone(field.help_text)

    def test_is_active_col_(self):
        active = self.model._meta.get_field(field_name='is_active')
        self.assertTrue(active.default)
        self.assertEqual(active.verbose_name, 'active')
        self.assertIsNotNone(active.help_text)

    def test_level_col_(self):
        level = self.model._meta.get_field('level')
        self.assertEqual(level.max_length, 8)
        self.assertIsNotNone(level.help_text)
        self.assertEqual(len(level.choices), 4)

        for i in level.choices:
            self.assertEqual(type(i), tuple)
            self.assertEqual(len(i), 2)
