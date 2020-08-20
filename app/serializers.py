from rest_framework import serializers
from .models import (Discipline, PaperType)
import uuid


class UUIDGenerator:
    def __init__(self, model):
        self.model = model

    def generate_uuid(self):
        generate = uuid.uuid4()
        try:
            self.model.objects.get(uuid__exact=generate)
        except self.model.DoesNotExist as e:
            return generate
        else:
            self.generate_uuid()


class DisciplineSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serialize Discipline Model Objects to json format
    """
    model = Discipline

    class Meta:
        model = Discipline
        fields = ('name', 'description')

    def create(self, validated_data):
        return Discipline.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            admin=self.context['request'].user,
            uuid=self.generate_uuid())


class DisciplineGetSerializer(serializers.ModelSerializer):
    """
    Serialize Discipline Model Objects to json format
    """

    class Meta:
        model = Discipline
        fields = ("admin", 'name', 'description', 'createdAt', 'updatedAt')


class PaperTypeSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serialize PaperType Model Objects to json format
    """
    model = PaperType

    class Meta:
        model = PaperType
        fields = ("admin", 'name', 'description')

    def create(self, validated_data):
        return PaperType.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            admin=self.context['request'].user,
            uuid=self.generate_uuid())
