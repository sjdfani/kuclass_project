from rest_framework import serializers
from .models import Major


class MajorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'


class MajorNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ('name',)
