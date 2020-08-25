from django.test import TestCase

from app.abstract import MinimalModel
from authapp.models import User
from order.models import Cancel, Order
from mixer.backend.django import mixer


class CancelModelTestCase(TestCase):
    """
    Tests for the Cancel Model
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = Cancel
        cls.data = mixer.blend(Cancel, reason="Too hard", deletedAt=None)

    def test_meta_class_for_the_model(self):
        meta = self.model._meta
        self.assertEqual(meta.model.__name__, 'Cancel')
        self.assertLogs(meta.db_table, 'Cancel')
        self.assertEqual(meta.verbose_name, 'Cancel')
        self.assertEqual(meta.verbose_name_plural, 'Cancels')
        self.assertEqual(meta.app_label, 'order')

    def test_no_of_fields(self):
        number = list(self.model._meta.get_fields())
        self.assertEqual(len(number), 9)

    def test_object_created_(self):
        objects = self.model.objects
        self.assertEqual(objects.all().count(), 1)
        self.assertEqual(objects.first().__str__(), 'Too hard')

    def test_is_subclass(self):
        self.assertTrue(issubclass(Cancel, MinimalModel))

    def test_can_update_(self):
        objects = self.model.objects.first()
        objects.reason = "Too easy"
        objects.save()
        self.assertEqual(objects.reason, 'Too easy')

    def test_can_delete_(self):
        objects = self.model.objects
        objects.first().delete()
        self.assertEqual(objects.all().count(), 0)

    def test_reason_column(self):
        reason = self.model._meta.get_field(field_name='reason')
        self.assertFalse(reason.null)
        self.assertEqual(reason.max_length, 200)

    def test_order_column(self):
        order = self.model._meta.get_field(field_name='order')
        self.assertFalse(order.null)

    def test_is_active(self):
        active = self.model._meta.get_field(field_name='is_active')
        self.assertTrue(active.default)

    def test_user_column(self):
        user = self.model._meta.get_field(field_name='user')
        self.assertFalse(user.null)

    def test_trash_method(self):
        objects = self.model.objects.first()
        self.assertTrue(objects.is_active)
        self.assertIsNone(objects.deletedAt)
        objects.trash()
        self.assertFalse(objects.is_active)
        self.assertIsNotNone(objects.deletedAt)
