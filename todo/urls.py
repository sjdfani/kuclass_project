from django.urls import path
from .views import (
    CreateJob, JobList, RetrieveUpdateDestroyJob,
)

app_name = 'todo'

urlpatterns = [
    path('create/', CreateJob.as_view(), name='create_job'),
    path('list/', JobList.as_view(), name='job_list'),
    path('list/<int:pk>/', RetrieveUpdateDestroyJob.as_view(),
         name='retrieve_update_destroy_job'),
]
