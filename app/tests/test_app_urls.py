from uuid import UUID

from django.urls import reverse, resolve
from app.views import (
    DeleteDisciplineAPIView, DisciplineCreateAPIView, RetrieveDisciplineAPIView,
    UpdateDisciplineAPIView, PaperTypeCreateAPIView, DeletePaperTypeAPIView, UpdatePaperTypeAPIView,
    RetrievePaperTypeAPIView, RetrieveAllActiveDisciplineAPIView, RetrieveDeletedDisciplineAPIView,
    RetrieveTotalAllDisciplineAPIView, RetrieveSpecificDisciplineAPIView, RetrieveSpecificPaperTypeAPIView,
    RetrieveTotalAllPaperTypeAPIView, RetrieveAllPaperTypeAPIView, RetrieveDeletedPaperTypeAPIView
)
from django.test import TestCase


class AppUrlsTestCase(TestCase):
    """
    All urls tests for the app django application
    """

    @classmethod
    def setUpTestData(cls):
        cls.current_app = 'app'
        cls.kwargs = {'uuid': UUID('217fe126-e175-11ea-87d0-0242ac130003')}
        cls.discipline_create = reverse(viewname='app:discipline-create', current_app=cls.current_app)
        cls.discipline_retrieve_deleted = reverse(viewname='app:discipline-retrieve-deleted',
                                                  current_app=cls.current_app)
        cls.discipline_retrieve_all = reverse(viewname='app:discipline-retrieve-all', current_app=cls.current_app)
        cls.discipline_retrieve_active = reverse(viewname='app:discipline-retrieve-active', current_app=cls.current_app)
        cls.paper_type_retrieve_deleted = reverse(viewname='app:paper-type-retrieve-deleted',
                                                  current_app=cls.current_app)
        cls.paper_type_retrieve_all = reverse(viewname='app:paper-type-retrieve-all', current_app=cls.current_app)
        cls.paper_type_retrieve_active = reverse(viewname='app:paper-type-retrieve-active', current_app=cls.current_app)
        cls.discipline_retrieve_admin = reverse(viewname='app:discipline-specific-admin', current_app=cls.current_app)
        cls.paper_type_retrieve_admin = reverse(viewname='app:paper-type-specific-admin', current_app=cls.current_app)
        cls.discipline_update = reverse(viewname='app:discipline-update', current_app=cls.current_app,
                                        kwargs=cls.kwargs)
        cls.discipline_delete = reverse(viewname='app:discipline-delete', current_app=cls.current_app,
                                        kwargs=cls.kwargs)
        cls.discipline_retrieve = reverse(viewname='app:discipline-retrieve', current_app=cls.current_app,
                                          kwargs=cls.kwargs)
        cls.paper_type_create = reverse(viewname='app:paper-type-create', current_app=cls.current_app)
        cls.paper_type_update = reverse(viewname='app:paper-type-update', current_app=cls.current_app,
                                        kwargs=cls.kwargs)
        cls.paper_type_delete = reverse(viewname='app:paper-type-delete', current_app=cls.current_app,
                                        kwargs=cls.kwargs)
        cls.paper_type_retrieve = reverse(viewname='app:paper-type-retrieve', current_app=cls.current_app,
                                          kwargs=cls.kwargs)

    def common_(self, view_name, func, url, url_name, app_name='app', args=None, kwargs=None):
        response = resolve(view_name)
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        self.assertEqual(response.route, url)
        self.assertEqual(response.func.view_class, func)
        self.assertEqual(response.url_name, url_name)
        self.assertIn(app_name, response.app_names)
        self.assertEqual(len(response.app_names), 1)
        self.assertEqual(response.namespace, app_name)
        self.assertIn(response.namespace, response.namespaces)
        self.assertEqual(response.kwargs, kwargs)
        self.assertEqual(response.args, args)
        self.assertEqual(response.app_name, app_name)

    def test_discipline_create_url(self):
        """
        Create discipline API Route
        """
        self.common_(view_name=self.discipline_create, func=DisciplineCreateAPIView, url_name='discipline-create',
                     url='api/v1/admin/discipline/create')

    def test_discipline_update_url(self):
        """
        Update discipline API Route
        """
        self.common_(view_name=self.discipline_update, func=UpdateDisciplineAPIView, url_name='discipline-update',
                     url='api/v1/admin/discipline/update/<uuid:uuid>', kwargs=self.kwargs)

    def test_discipline_retrieve_url(self):
        """
        Retrieve discipline API Route
        """
        self.common_(view_name=self.discipline_retrieve, func=RetrieveDisciplineAPIView, url_name='discipline-retrieve',
                     url='api/v1/admin/discipline/retrieve/get/<uuid:uuid>', kwargs=self.kwargs)

    def test_discipline_retrieve_all_url(self):
        """
        Retrieve all (active & deleted) discipline API Route
        """
        self.common_(view_name=self.discipline_retrieve_all, func=RetrieveTotalAllDisciplineAPIView,
                     url_name='discipline-retrieve-all',
                     url='api/v1/admin/discipline/retrieve/all/')

    def test_retrieve_paper_type_admin(self):
        """
        Retrieve admin specific paper types
        """
        self.common_(view_name=self.discipline_retrieve_admin, func=RetrieveSpecificDisciplineAPIView,
                     url_name='discipline-specific-admin',
                     url='api/v1/admin/discipline/retrieve/admin')

    def test_discipline_retrieve_all_active_url(self):
        """
        Retrieve all (active) discipline API Route
        """
        self.common_(view_name=self.discipline_retrieve_active, func=RetrieveAllActiveDisciplineAPIView,
                     url_name='discipline-retrieve-active', url='api/v1/admin/discipline/retrieve/all/active')

    def test_discipline_retrieve_all_deleted_url(self):
        """
        Retrieve all (deleted) discipline API Route
        """
        self.common_(view_name=self.discipline_retrieve_deleted, func=RetrieveDeletedDisciplineAPIView,
                     url_name='discipline-retrieve-deleted', url='api/v1/admin/discipline/retrieve/all/deleted')

    def test_discipline_delete_url(self):
        """
        Delete discipline API Route
        """
        self.common_(view_name=self.discipline_delete, func=DeleteDisciplineAPIView, url_name='discipline-delete',
                     url='api/v1/admin/discipline/delete/<uuid:uuid>', kwargs=self.kwargs)

    def test_paper_type_create_url(self):
        """
        Create a paper type API Route
        """
        self.common_(view_name=self.paper_type_create, func=PaperTypeCreateAPIView, url_name='paper-type-create',
                     url='api/v1/admin/paper/type/create')

    def test_paper_type_retrieve_url(self):
        """
        Retrieve a paper type API Route
        """
        self.common_(view_name=self.paper_type_retrieve, func=RetrievePaperTypeAPIView, url_name='paper-type-retrieve',
                     url='api/v1/admin/paper/type/retrieve/get/<uuid:uuid>', kwargs=self.kwargs)

    def test_paper_type_retrieve_all_url(self):
        """
        Retrieve all (active & deleted) paper_type API Route
        """
        self.common_(view_name=self.paper_type_retrieve_all, func=RetrieveTotalAllPaperTypeAPIView,
                     url_name='paper-type-retrieve-all', url='api/v1/admin/paper/type/retrieve/all/')

    def test_paper_type_retrieve_all_active_url(self):
        """
        Retrieve all (active) paper_type API Route
        """
        self.common_(view_name=self.paper_type_retrieve_active, func=RetrieveAllPaperTypeAPIView,
                     url_name='paper-type-retrieve-active',
                     url='api/v1/admin/paper/type/retrieve/all/active')

    def test_paper_type_retrieve_all_deleted_url(self):
        """
        Retrieve all (deleted) paper_type API Route
        """
        self.common_(view_name=self.paper_type_retrieve_deleted, func=RetrieveDeletedPaperTypeAPIView,
                     url_name='paper-type-retrieve-deleted',
                     url='api/v1/admin/paper/type/retrieve/all/deleted')

    def test_paper_type_update_url(self):
        """
        Update a paper type API Route
        """
        self.common_(view_name=self.paper_type_update, func=UpdatePaperTypeAPIView, url_name='paper-type-update',
                     url='api/v1/admin/paper/type/update/<uuid:uuid>', kwargs=self.kwargs)

    def test_paper_type_delete_url(self):
        """
        Delete a paper type API Route
        """
        self.common_(view_name=self.paper_type_delete, func=DeletePaperTypeAPIView, url_name='paper-type-delete',
                     url='api/v1/admin/paper/type/delete/<uuid:uuid>', kwargs=self.kwargs)

    def test_retrieve_admin_specific_paper_type(self):
        """
        Retrieve admin specific paper types
        """
        self.common_(view_name=self.paper_type_retrieve_admin, func=RetrieveSpecificPaperTypeAPIView,
                     url="api/v1/admin/paper/type/retrieve/admin", url_name="paper-type-specific-admin")
