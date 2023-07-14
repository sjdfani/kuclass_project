from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonsByMajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name', 'master_name', 'unit')
