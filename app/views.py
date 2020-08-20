from django.http import QueryDict
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authapp.permissions.permissions import IsMasterAdmin, IsUser
from .serializers import DisciplineSerializer, PaperTypeSerializer, DisciplineGetSerializer
from .models import Discipline, PaperType
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
from rest_framework import status


# Create discipline
class DisciplineCreateAPIView(CreateAPIView):
    """
    Create a new discipline API
    """
    serializer_class = DisciplineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']
    model = Discipline

    def get_queryset(self):
        return self.model.objects.all()


# get discipline
class RetrieveDisciplineAPIView(RetrieveAPIView):
    """
    Get information of a single discipline
    """
    http_method_names = ['get']
    serializer_class = DisciplineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Discipline
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


# get discipline
class RetrievePaperTypeAPIView(RetrieveAPIView):
    """
    Get information of a single paper type
    """
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']
    serializer_class = DisciplineGetSerializer
    authentication_classes = (TokenAuthentication,)
    model = PaperType
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


class RetrieveSpecificDisciplineAPIView(ListAPIView):
    """
    Get information all create by admin specific disciplines
    """
    http_method_names = ['get']
    serializer_class = DisciplineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Discipline

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True, admin=self.request.user)


class RetrieveAllActiveDisciplineAPIView(ListAPIView):
    """
    Get information of a all active disciplines
    """
    http_method_names = ['get']
    serializer_class = DisciplineGetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Discipline

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


class RetrieveDeletedDisciplineAPIView(ListAPIView):
    """
    Get information of a all deleted discipline
    """
    http_method_names = ['get']
    serializer_class = DisciplineGetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Discipline

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=False)


class RetrieveTotalAllDisciplineAPIView(ListAPIView):
    """
    Get information of a all deleted or active discipline
    """
    http_method_names = ['get']
    serializer_class = DisciplineGetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Discipline

    def get_queryset(self):
        return self.model.objects.all()


# update discipline
class UpdateDisciplineAPIView(UpdateAPIView):
    """
    Update information of a single discipline
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DisciplineSerializer
    authentication_classes = (TokenAuthentication,)
    model = Discipline
    http_method_names = ['put', 'patch']
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


# delete discipline
class DeleteDisciplineAPIView(DestroyAPIView):
    """
    Delete a single discipline information from the server
    """
    http_method_names = ['delete']
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    model = Discipline
    serializer_class = DisciplineSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)

    def perform_destroy(self, instance):
        instance.trash()


# Create paper_type
class PaperTypeCreateAPIView(CreateAPIView):
    """
    Create a new paper type
    """
    http_method_names = ['post']
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    serializer_class = PaperTypeSerializer
    authentication_classes = (TokenAuthentication,)
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all()


# get paper_type
class RetrieveSpecificPaperTypeAPIView(ListAPIView):
    """
    Get information all create by admin specific paper type
    """
    http_method_names = ['get']
    authentication_classes = (TokenAuthentication,)
    serializer_class = PaperTypeSerializer
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True, admin=self.request.user)


class RetrieveAllPaperTypeAPIView(ListAPIView):
    """
    Get information of a all active paper type
    """
    serializer_class = DisciplineGetSerializer
    http_method_names = ['get']
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    authentication_classes = (TokenAuthentication,)
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


class RetrieveDeletedPaperTypeAPIView(ListAPIView):
    """
    Get information of a all deleted paper type
    """
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get']
    serializer_class = DisciplineGetSerializer
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=False)


class RetrieveTotalAllPaperTypeAPIView(ListAPIView):
    """
    Get information of a all deleted or active paper type
    """
    serializer_class = DisciplineGetSerializer
    http_method_names = ['get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all()


# Update paper_type
class UpdatePaperTypeAPIView(UpdateAPIView):
    """
    Update a single paper type from the server api view
    """

    serializer_class = PaperTypeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    http_method_names = ['put', 'patch']
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)


# delete paper_type
class DeletePaperTypeAPIView(DestroyAPIView):
    """
    Retrieve a single paper type from the server api view
    """

    serializer_class = PaperTypeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMasterAdmin)
    http_method_names = ['delete']
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
    model = PaperType

    def get_queryset(self):
        return self.model.objects.all().filter(is_active=True)

    def perform_destroy(self, instance):
        instance.trash()

