from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Lesson
from .serializers import (
    LessonSerializer, LessonsByMajorSerializer,
)


class CreateLesson(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonListByMajor(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonsByMajorSerializer

    def get_queryset(self):
        major_name = self.kwargs['major']
        return Lesson.objects.filter(major__name=major_name, status=True)


class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
