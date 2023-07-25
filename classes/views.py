from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Class
from .serializers import (
    CreateClassSerializer, DeleteClassSerializer, ClassSerializer,
    UpdateClassSerializer, UpdateMultiClassSerializer,
)
from django.db.models import Q


class CreateClass(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateClassSerializer
    queryset = Class.objects.all()


class DeleteClass(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = DeleteClassSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class RetrieveUpdateClass(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClassSerializer
        return UpdateClassSerializer

    def get_queryset(self):
        return Class.objects.filter(user=self.request.user, status=True)


class UpdateMultiClass(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        serializer = UpdateMultiClassSerializer(
            data=request.data, context={'request': request, 'pk': pk}
        )
        if serializer.is_valid(raise_exception=True):
            repeat = self.kwargs['repeat']
            serializer.save(pk, repeat)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllClassesByUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        return Class.objects.filter(user=self.request.user, status=True)


class GetClassesByUserWithDate(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        from_ = self.kwargs["from"]
        to_ = self.kwargs["to"]
        lookup = Q(date_of_day__gte=from_) & Q(date_of_day__lte=to_)
        return Class.objects.filter(lookup, status=True)
