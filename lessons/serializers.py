from rest_framework import serializers
from .models import Lesson
from major.serializers import MajorListSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
