from django.test import TestCase
from app.models import Alert
from authapp.models import User
from mixer.backend.django import mixer
from app.choices import AlertChoices


class AlertModelTestCase(TestCase):
    """ Tests for the Alert Model """

    @classmethod
    def setUpTestData(cls):
        cls.model = Alert
        cls.deleter = mixer.blend(User, user_type='Master', is_superuser=True, is_staff=True, is_active=True)
        cls.default = 'Title 101'
        cls.data = mixer.blend(cls.model, title=cls.default, is_active=True, deletedAt=None,
                               default=AlertChoices.REVIEW, deleted_by=None)

    def test_objects_created_(self):
        objects = self.model.objects.all()
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().title, self.default)
        self.assertIsInstance(objects.first().admin, User)
        self.assertEqual(objects.first().__str__(), self.default)

    def test_meta_class_for_the_model(self):
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Alert')
        self.assertEqual(meta.db_table, 'Alert')
        self.assertIn(member='-createdAt', container=list(meta.ordering))
        self.assertEqual(meta.verbose_name_plural, 'Alerts')
        self.assertEqual(meta.verbose_name, 'Alert')
        self.assertEqual(meta.app_label, 'app')

    def test_update_objects(self):
        objects = self.model.objects.first()
        objects.title = 'Title 202'
        objects.save()
        self.assertEqual(objects.title, 'Title 202')

    def test_no_of_fields(self):
        fields = list(self.model._meta.get_fields(include_hidden=True, include_parents=True))
        self.assertEqual(len(fields), 14)

    def test_title_column_(self):
        title = self.model._meta.get_field(field_name='title')
        self.assertFalse(title.null)
        self.assertIsNotNone(title.help_text)
        self.assertEqual(title.max_length, 30)

    def test_description_column_(self):
        description = self.model._meta.get_field(field_name='description')
        self.assertIsNotNone(description.help_text)

    def test_status_column_(self):
        status = self.model._meta.get_field(field_name='status')
        self.assertIsNotNone(status.help_text)
        self.assertEqual(status.max_length, 10)
        self.assertFalse(status.null)
        self.assertEqual(len(list(status.choices)), 4)
        self.assertIsNotNone(status.default)

        for i in status.choices:
            self.assertEqual(len(i), 2)
            self.assertEqual(type(i), tuple)

    def test_type_column_(self):
        _type = self.model._meta.get_field(field_name='_type')
        self.assertEqual(_type.max_length, 12)
        self.assertFalse(_type.null)
        self.assertIsNotNone(_type.help_text)

        for i in _type.choices:
            self.assertEqual(len(i), 2)
            self.assertEqual(type(i), tuple)

    def test_from_column_(self):
        _from = self.model._meta.get_field(field_name='_from')
        self.assertFalse(_from.null)
        self.assertIsNotNone(_from.help_text)

    def test_to_column_(self):
        to = self.model._meta.get_field(field_name='to')
        self.assertFalse(to.null)
        self.assertIsNotNone(to.help_text)

    def test_is_active_column_(self):
        active = self.model._meta.get_field(field_name='is_active')
        self.assertTrue(active.default)
        self.assertIsNotNone(active.help_text)

    def test_can_delete_alert_(self):
        objects = self.model.objects.first()
        self.assertIsNone(objects.deletedAt)
        self.assertIsNone(objects.deleted_by)
        objects.deleted_by = self.deleter
        objects.save()
        objects.trash()
        self.assertIsNotNone(objects.deleted_by)
        self.assertIsNotNone(objects.deletedAt)
        self.assertEqual(len(self.model.objects.all().filter(is_active=True)), 0)
        self.assertEqual(len(self.model.objects.all().filter(is_active=False)), 1)

    def test_deleted_by_column(self):
        deleted = self.model._meta.get_field(field_name='deleted_by')
        self.assertTrue(deleted.null)

    def test_admin_column(self):
        admin = self.model._meta.get_field(field_name='admin')
        self.assertFalse(admin.null)
