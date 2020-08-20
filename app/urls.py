from django.urls import path, include

from .views import (
    DeleteDisciplineAPIView, DisciplineCreateAPIView, RetrieveDisciplineAPIView,
    UpdateDisciplineAPIView, PaperTypeCreateAPIView, DeletePaperTypeAPIView, UpdatePaperTypeAPIView,
    RetrievePaperTypeAPIView, RetrieveAllActiveDisciplineAPIView, RetrieveDeletedDisciplineAPIView,
    RetrieveTotalAllDisciplineAPIView, RetrieveSpecificDisciplineAPIView, RetrieveSpecificPaperTypeAPIView,
    RetrieveTotalAllPaperTypeAPIView, RetrieveAllPaperTypeAPIView, RetrieveDeletedPaperTypeAPIView
)

app_name = "app"

urlpatterns = [

    # All route paths # discipline
    path('discipline/', include([
        path('create', DisciplineCreateAPIView.as_view(), name="discipline-create"),

        path('retrieve/', include([
            path('all/', include([
                path('active', RetrieveAllActiveDisciplineAPIView.as_view(), name='discipline-retrieve-active'),
                path('', RetrieveTotalAllDisciplineAPIView.as_view(), name='discipline-retrieve-all'),
                path('deleted', RetrieveDeletedDisciplineAPIView.as_view(),
                     name='discipline-retrieve-deleted')
            ])),
            path('get/<uuid:uuid>', RetrieveDisciplineAPIView.as_view(), name='discipline-retrieve'),
            path('admin', RetrieveSpecificDisciplineAPIView.as_view(), name='discipline-specific-admin'),
        ])),

        path('update/<uuid:uuid>', UpdateDisciplineAPIView.as_view(), name='discipline-update'),
        path('delete/<uuid:uuid>', DeleteDisciplineAPIView.as_view(), name='discipline-delete'),

    ])),

    # All route paths # paper_type
    path('paper/type/', include([
        path('create', PaperTypeCreateAPIView.as_view(), name="paper-type-create"),
        path('retrieve/', include([
            path('all/', include([
                path('active', RetrieveAllPaperTypeAPIView.as_view(), name='paper-type-retrieve-active'),
                path('', RetrieveTotalAllPaperTypeAPIView.as_view(), name='paper-type-retrieve-all'),
                path('deleted', RetrieveDeletedPaperTypeAPIView.as_view(),
                     name='paper-type-retrieve-deleted')
            ])),
            path('get/<uuid:uuid>', RetrievePaperTypeAPIView.as_view(), name="paper-type-retrieve"),
            path('admin', RetrieveSpecificPaperTypeAPIView.as_view(), name='paper-type-specific-admin'),
        ])),
        path('update/<uuid:uuid>', UpdatePaperTypeAPIView.as_view(), name="paper-type-update"),
        path('delete/<uuid:uuid>', DeletePaperTypeAPIView.as_view(), name="paper-type-delete"),
    ])),
]
