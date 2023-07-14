from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Class
from .serializers import (
    CreateClassSerializer,
)


class CreateClass(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateClassSerializer
    queryset = Class.objects.all()
