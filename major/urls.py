from django.urls import path
from .views import (
    CreateMajor, MajorNameList, MajorRetrieveUpdateDestroy,
)

app_name = 'major'

urlpatterns = [
    path('create/', CreateMajor.as_view(), name='create'),
    path('list/<str:grade>/', MajorNameList.as_view(), name='list'),
    path('list/<int:pk>/', MajorRetrieveUpdateDestroy.as_view(),
         name='retrieve_update_destroy_major'),
]
