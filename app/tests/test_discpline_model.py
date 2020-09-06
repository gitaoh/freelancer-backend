from django.test import TestCase
from mixer.backend.django import mixer
from app.models import Discipline


class DisciplineModelTestcase(TestCase):
    """
    All tests for the Discipline Model in the app django application
    """

    @classmethod
    def setUpTestData(cls):
        """
        Data to be used on every testcase
        """
        cls.model = Discipline
        cls.default = 'DisciplineOne'
        cls.model_data = mixer.blend(cls.model, name=cls.default)

    def test_model_object_was_created_successfully(self):
        """
        Testing whether we can create a Discipline Model object to the database
        """
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().name, self.default)
        self.assertEqual(objects.first().__str__(), self.default)

    def test_model_object_has_multiple_objects_created_successfully(self):
        """
        Test that we can create multiple Discipline model object
        """
        names = ['name1', 'name2', 'name3']

        # Create four Objects
        mixer.cycle(count=3).blend(self.model, name=(nm for nm in names))
        objects = self.model.objects

        # If Success 4 because of setupData creates a model before this test is executed
        self.assertEqual(objects.count(), 4)
        self.assertEqual(objects.all().filter(name__startswith='name').count(), 3)

        # check all unique names
        for i in range(len(names) + 1):
            if i == 0:
                continue
            self.assertEqual(objects.all().filter(name__endswith=f'{i}').count(), 1)

    def test_model_object_has_multiple_objects_have_unique_names(self):
        """
        Test that we create object with unique names, uuid
        """
        names = ['name1', 'name2', 'name3']

        # Create four Objects
        mixer.cycle(count=3).blend(self.model, name=(nm for nm in names))
        objects = self.model.objects
        self.assertEqual(objects.count(), 4)

    def test_name_column(self):
        """
        Test the configured fields for the name column in the model
        """
        name = self.model._meta.get_field(field_name='name')
        self.assertEqual(name.max_length, 200)
        self.assertTrue(name.unique)

    def test_number_of_fields_in_the_models(self):
        """
        Test the number of fields/column allowed to be in the model
        """
        fields = list(self.model._meta.get_fields(include_hidden=True, include_parents=True))
        self.assertEqual(len(fields), 9)

    def test_is_active_column(self):
        active = self.model._meta.get_field(field_name='is_active')
        self.assertTrue(active.default)
        self.assertFalse(active.null)

    def test_default_model_data_modified(self):
        """
        Test that we ca modify created discipline object
        """
        objects = self.model.objects.first()
        objects.name = "Modified name"
        objects.save()
        self.assertEqual(objects.name, 'Modified name')

    def test_we_delete_existing_objects(self):
        """
         Test that we can successfully delete an existing object on the database
        """
        mixer.cycle(10).blend(self.model)
        objects = self.model.objects
        self.assertEqual(objects.count(), 11)
        # Delete 1 objects
        objects.first().delete()
        # Deleted 1 object
        self.assertEqual(objects.count(), 10)

    def test_meta_class_is_as_configured(self):
        """
        Custom meta class has the default fields configured
        """
        meta = self.model._meta
        # meta.model._meta  == 'app.discipline'
        self.assertEqual(meta.verbose_name, 'Discipline')
        self.assertEqual(meta.model.__name__, 'Discipline')
        self.assertEqual(meta.db_table, 'Discipline')
        self.assertEqual(meta.verbose_name_plural, 'Disciplines')
        self.assertFalse(meta.abstract)

    # def test_name_field_has_to_be_unique(self):
    #     from django.db.utils import IntegrityError
    #     """
    #     Test that no discipline should have it's unique name
    #     """
    #     pass
    #     try:
    #         mixer.blend(self.model, name=self.default)
    #     except Exception as e:
    #         print(e)
    #         self.assertRaises(IntegrityError)
    #         self.assertEqual(e, IntegrityError)
