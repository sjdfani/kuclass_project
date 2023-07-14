from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Lesson
from .serializers import (
    LessonSerializer,
)


class CreateLesson(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
