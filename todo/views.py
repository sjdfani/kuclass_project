from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import (
    JobSerializer, CreateJobSerializer, RetrieveUpdateDestroyJobSerializer,
)


class CreateJob(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateJobSerializer
    queryset = Job.objects.all()


class JobList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)


class RetrieveUpdateDestroyJob(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobSerializer
        return RetrieveUpdateDestroyJobSerializer

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)
