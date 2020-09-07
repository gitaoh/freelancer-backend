from rest_framework import serializers
from .models import (Discipline, PaperType, Alert)
from recycle.uuid_generator import UUIDGenerator


class DisciplineSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serialize Discipline Model Objects to json format
    """
    model = Discipline

    class Meta:
        model = Discipline
        fields = ('name', 'description', 'level', 'price')

    def create(self, validated_data):
        return Discipline.objects.create(
            **validated_data,
            admin=self.context['request'].user,
            uuid=self.generate_uuid())


class DisciplineGetSerializer(serializers.ModelSerializer):
    """
    Serialize Discipline Model Objects to json format
    """

    class Meta:
        model = Discipline
        fields = (
            'admin', 'uuid', 'is_active', 'name', 'description', 'level', 'price', 'createdAt', 'updatedAt', 'valid')


class PaperTypeSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serialize PaperType Model Objects to json format
    """
    model = PaperType

    class Meta:
        model = PaperType
        fields = ('name', 'description', 'level', 'price')

    def create(self, validated_data):
        return PaperType.objects.create(
            **validated_data,
            admin=self.context['request'].user,
            uuid=self.generate_uuid())


class AlertModelSerializer(serializers.ModelSerializer, UUIDGenerator):
    """
    Serialize Alert Model objects to json format
    """
    model = Alert

    class Meta:
        model = Alert
        fields = ['title', 'description', '_from', 'to', '_type', 'status']

    def create(self, validated_data):
        return self.model.objects.create(
            **validated_data,
            admin=self.context['request'].user,
            uuid=self.generate_uuid()
        )


class AlertModelSerialize(serializers.ModelSerializer):
    class Meta:
        model = Alert
        exclude = ['deletedAt', 'is_active', 'deleted_by']


class AlertModelDeletedSerialize(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
