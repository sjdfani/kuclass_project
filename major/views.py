from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Major
from .serializers import (
    MajorListSerializer, MajorNameListSerializer
)


class CreateMajor(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = MajorListSerializer
    queryset = Major.objects.all()


class MajorNameList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MajorNameListSerializer

    def get_queryset(self):
        grade = self.kwargs.get('grade')
        return Major.objects.filter(grade=grade, status=True)


class MajorRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = MajorListSerializer
    queryset = Major.objects.all()
