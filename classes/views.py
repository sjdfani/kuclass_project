from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Class
from .serializers import (
    CreateClassSerializer, DeleteClassSerializer,
)


class CreateClass(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateClassSerializer
    queryset = Class.objects.all()


class DeleteClass(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = DeleteClassSerializer(
            request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return Response(message, status=status.HTTP_204_NO_CONTENT)
