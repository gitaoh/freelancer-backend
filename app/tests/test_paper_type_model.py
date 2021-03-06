from mixer.backend.django import mixer
from django.test import TestCase
from app.models import PaperType
from authapp.models import User


class PaperTypeModelTestcase(TestCase):
    """
    All tests for the PaperType Model in the app django application
    """

    @classmethod
    def setUpTestData(cls):
        """
        Data to be used on every testcase
        """
        cls.default = 'paper 101'
        cls.user = mixer.blend(User, username="joseph", user_type="MASTER")
        cls.model = PaperType
        cls.model_data = mixer.blend(PaperType, name=cls.default, admin=cls.user)

    def test_meta_class_for_the_model(self):
        """
        Custom meta class has the default fields configured
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.verbose_name, 'PaperType')
        self.assertEqual(meta.verbose_name_plural, 'PaperTypes')
        self.assertEqual(meta.db_table, 'PaperType')
        self.assertEqual(meta.model.__name__, 'PaperType')

    def test_default_model_creation(self):
        """
        setUpTestData creates a model successfully to be used by every test
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().name, self.default)
        self.assertEqual(objects.first().__str__(), self.default)

    def test_can_update_default_object(self):
        """
        Test that we can update an existing object object
        """
        objects = self.model.objects.first()
        objects.name = "New paper 101"
        objects.save()
        self.assertEqual(objects.name, 'New paper 101')

    def test_can_delete_default_object(self):
        """
        Test that we can delete an existing object object
        """
        objects = self.model.objects
        objects.first().delete()
        self.assertEqual(objects.count(), 0)

    def test_number_of_fields_in_the_model(self):
        """
        Count of all the fields create by this model
        """
        fields = list(self.model._meta.get_fields())
        self.assertEqual(len(fields), 9)

    def test_is_active_column(self):
        active = self.model._meta.get_field(field_name='is_active')
        self.assertTrue(active.default)
        self.assertFalse(active.null)

    def test_name_column(self):
        """
        Test the configured fields for the name column in the model
        """
        name = self.model._meta.get_field(field_name='name')
        self.assertTrue(name.unique)
        self.assertEqual(name.max_length, 200)

    def test_description_column(self):
        """
        Test the configured fields for the description column in the model
        """
        name = self.model._meta.get_field(field_name='description')
        self.assertTrue(name)

    def test_name_field_has_to_be_unique(self):
        from django.db.utils import IntegrityError
        """
        Test that no discipline should have it's unique name
        """
        pass
        # try:
        #     mixer.blend(self.model, name=self.default)
        # except Exception as e:
        #     print(e)
        #     self.assertRaises(IntegrityError)
        #     self.assertEqual(e, IntegrityError)
