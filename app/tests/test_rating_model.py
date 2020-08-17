from django.test import TestCase
from app.models import Rating
from authapp.models import User
from mixer.backend.django import mixer


class RatingModelTestcase(TestCase):
    """
    All tests for the rating model in the app django application
    """

    @classmethod
    def setUpTestData(cls):
        """
        Data to be used on every testcase
        """
        cls.default = 5
        cls.user = mixer.blend(User, username='joseph')
        cls.model = Rating
        cls.model_data = mixer.blend(cls.model, rate=cls.default, client=cls.user)

    def test_meta_class_for_the_model(self):
        """
        Test this model custom configured meta class
        """
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Rating')
        self.assertEqual(meta.verbose_name, 'Rating')
        self.assertEqual(meta.verbose_name_plural, 'Ratings')
        self.assertEqual(meta.db_table, 'Rating')

    def test_fields_in_this_model(self):
        """
        Test the total number configured field/columns
        """
        fields = list(self.model._meta.get_fields())
        self.assertEqual(len(fields), 7)

    def test_the_rate_column(self):
        """
        Test configured fields in the rate column in the model
        """
        rate = self.model._meta.get_field(field_name='rate')
        self.assertEqual(len(rate.validators), 2)

    def test_the_client_column(self):
        """
        Test configured fields in the client column in the model
        """
        client = self.model._meta.get_field(field_name='client')
        self.assertTrue(client.null)
        self.assertIsNone(client.default)

    def test_default_test_data_was_created(self):
        """
        setUpTestData creates a model successfully to be used by every test
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().rate, self.default)
        self.assertEqual(objects.first().__str__(), f'{self.default}, {User.objects.first().username}')

    def test_can_delete_existing_objects(self):
        """
        Test Deleting objects from the database model
        """
        objects = self.model.objects
        objects.first().delete()
        self.assertEqual(objects.count(), 0)

    # def test_update_default_data(self):
    #     """
    #     Test Updating objects from the database model
    #     """
    #     objects = self.model.objects.first()
    #     objects.rate = 4
    #     objects.save()
    #     self.assertEqual(objects.rate, 4)
