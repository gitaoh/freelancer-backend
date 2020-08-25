from django.test import TestCase

from app.abstract import MinimalModel
from order.models import Order, Writer
from authapp.models import User
from mixer.backend.django import mixer


class OrderModelTestCase(TestCase):
    """
    All tests for the order model in the order django application
    """

    @classmethod
    def setUpTestData(cls):
        cls.model = Order
        cls.default = {'username': 'joseph', 'discipline': "discipline 101", 'paper': 'paper 101'}
        cls.user = mixer.blend(User, username=cls.default['username'])
        cls.writer = mixer.blend(Writer, username=cls.default['username'])
        cls.data = mixer.blend(Order, is_paper=True, user=cls.user, writer=cls.writer, revision=False, deletedAt=None,
                               discipline=cls.default['discipline'], paper_type=cls.default['paper'])

    def test_meta_class_properties(self):
        meta = self.model._meta
        self.assertFalse(meta.abstract)
        self.assertEqual(meta.model.__name__, 'Order')
        self.assertEqual(meta.verbose_name, 'Order')
        self.assertEqual(meta.verbose_name_plural, 'Orders')
        self.assertEqual(meta.db_table, 'Order')

    def test_number_or_fields_(self):
        """
        Allow fields in the model
        """
        fields = len(list(self.model._meta.get_fields()))
        self.assertEqual(fields, 36)

    def test_is_subclass_(self):
        """
        Order model should be a subclass of MinimalModel
        """
        self.assertTrue(issubclass(Order, MinimalModel))

    def test_object_data_created_(self):
        objects = self.model.objects
        self.assertEqual(objects.count(), 1)
        self.assertEqual(objects.first().__str__(), f"{self.default['discipline']}, {self.default['paper']}")

    def test_update_object_(self):
        objects = self.model.objects.first()
        objects.discipline = 'New discipline'
        objects.save()
        self.assertEqual(objects.discipline, 'New discipline')

    def test_delete_object_(self):
        objects = self.model.objects.first()
        self.assertIsNone(objects.deletedAt)
        self.assertTrue(objects.is_paper)
        objects.trash()
        self.assertIsNotNone(objects.deletedAt)
        self.assertFalse(objects.is_paper)

    def paper_revision_all_(self, verbose_name, field):
        fields = self.model._meta.get_field(field)
        self.assertEqual(fields.verbose_name, verbose_name)
        if field == 'is_paper':
            self.assertTrue(fields.default)
        else:
            self.assertFalse(fields.default)
        self.assertIsNotNone(fields.help_text)

    def test_is_paper_column_(self):
        self.paper_revision_all_(verbose_name='is_paper', field='is_paper')

    def test_revision_column_(self):
        self.paper_revision_all_(verbose_name='revision', field='revision')

    def test_dispute_column_(self):
        self.paper_revision_all_(verbose_name='dispute', field='dispute')

    def test_confirmed_column_(self):
        self.paper_revision_all_(verbose_name='confirmed', field='confirmed')

    def test_paid_column_(self):
        self.paper_revision_all_(verbose_name='paid', field='paid')

    def test_smart_column_(self):
        self.paper_revision_all_(verbose_name='is_smart', field='smart')

    def test_cost_column_(self):
        cost = self.model._meta.get_field('cost')
        self.assertEqual(cost.default, 0)
        self.assertIsNotNone(cost.help_text)

    def test_progressive_column_(self):
        prog = self.model._meta.get_field('progressive')
        self.assertFalse(prog.default)
        self.assertIsNotNone(prog.help_text)

    def test_native_column_(self):
        native = self.model._meta.get_field('native')
        self.assertFalse(native.default)
        self.assertIsNotNone(native.help_text)

    def test_charts_column_(self):
        charts = self.model._meta.get_field(field_name='charts')
        self.assertEqual(charts.default, 0)
        self.assertIsNotNone(charts.help_text)

    def test_sources_column_(self):
        sources = self.model._meta.get_field(field_name='sources')
        self.assertEqual(sources.default, 0)
        self.assertIsNotNone(sources.help_text)

    def test_pages_column_(self):
        pages = self.model._meta.get_field(field_name='pages')
        self.assertEqual(pages.default, 0)
        self.assertIsNotNone(pages.help_text)

    def test_deadline_column_(self):
        deadline = self.model._meta.get_field(field_name='deadline')
        self.assertIsNotNone(deadline.default)
        self.assertIsNotNone(deadline.help_text)

    def test_instructions_column_(self):
        instructions = self.model._meta.get_field(field_name='instructions')
        self.assertIsNotNone(instructions.help_text)

    def test_additional_materials_column_(self):
        additional = self.model._meta.get_field(field_name='additional_materials')
        self.assertTrue(additional)

    def test_title_column_(self):
        title = self.model._meta.get_field(field_name='title')
        self.assertEqual(title.verbose_name, 'title')
        self.assertEqual(title.max_length, 200)
        self.assertFalse(title.null)
        self.assertIsNotNone(title.help_text)

    def test_payment_url_column_(self):
        url = self.model._meta.get_field(field_name='payments_url')
        self.assertTrue(url.null)
        self.assertTrue(url.unique)
        self.assertIsNotNone(url.help_text)
        self.assertEqual(url.verbose_name, 'payment_url')

    def choices_column_(self, field, choices, length):
        fields = self.model._meta.get_field(field_name=field)
        self.assertEqual(fields.max_length, length)
        self.assertEqual(len(fields.choices), choices)
        self.assertIsNotNone(fields.help_text)
        self.assertEqual(fields.default, fields.choices[1][0])

        for i in fields.choices:
            self.assertEqual(type(i), tuple)
            self.assertEqual(len(i), 2)

    def test_status_column_(self):
        self.choices_column_(field='status', choices=7, length=10)

    def test_preference_column_(self):
        self.choices_column_(field='preference', choices=4, length=20)

    def test_powerpoint_column_(self):
        ppt = self.model._meta.get_field(field_name='powerpoint')
        self.assertEqual(ppt.default, 0)
        self.assertIsNotNone(ppt.help_text)

    def test_spacing_column_(self):
        self.choices_column_(field='spacing', choices=3, length=6)

    def test_format_column_(self):
        self.choices_column_(field='format', choices=5, length=16)

    def test_academic_column_(self):
        self.choices_column_(field='academic', choices=6, length=17)

    def test_discipline_column_(self):
        discipline = self.model._meta.get_field(field_name='discipline')
        self.assertEqual(discipline.verbose_name, 'discipline')
        self.assertEqual(discipline.max_length, 200)
        self.assertFalse(discipline.null)
        self.assertIsNotNone(discipline.help_text)

    def test_paper_type_column_(self):
        paper_type = self.model._meta.get_field(field_name='paper_type')
        self.assertEqual(paper_type.verbose_name, 'paper_type')
        self.assertEqual(paper_type.max_length, 200)
        self.assertFalse(paper_type.null)
        self.assertIsNotNone(paper_type.help_text)

    def test_user_column_(self):
        user = self.model._meta.get_field(field_name='user')
        # self.assertIsNone(user.default)
        self.assertFalse(user.null)
        self.assertIsNotNone(user.help_text)
        self.assertEqual(self.model.objects.first().user.username, User.objects.first().username)

    def test_user_column_is_a_User_instance_(self):
        self.assertTrue(isinstance(self.model.objects.first().user, User))

    def test_writer_column_(self):
        writer = self.model._meta.get_field(field_name='writer')
        # self.assertIsNone(writer.default)
        self.assertTrue(writer.null)
        self.assertIsNotNone(writer.help_text)
        self.assertEqual(self.model.objects.first().writer.username, Writer.objects.first().username)

    def test_writer_column_is_a_Writer_instance_(self):
        self.assertTrue(isinstance(self.model.objects.first().writer, Writer))

    def test_is_approved_column(self):
        approved = self.model._meta.get_field(field_name='is_approved')
        self.assertFalse(approved.default)
        self.assertEqual(approved.verbose_name, 'is_approved')
        self.assertIsNotNone(approved.help_text)

    def test_approve_a_paper(self):
        order = self.model.objects.first()
        self.assertFalse(order.is_approved)
        order.approve()
        self.assertTrue(order.is_approved)

    def test_disapprove_a_paper(self):
        order = self.model.objects.first()
        self.assertFalse(order.is_approved)
        order.approve()
        self.assertTrue(order.is_approved)
        order.un_approve()
        self.assertFalse(order.is_approved)
