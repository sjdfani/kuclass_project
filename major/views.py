from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from .models import Major
from .serializers import (
    MajorListSerializer
)


class CreateMajor(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = MajorListSerializer
    queryset = Major.objects.all()
