from django.urls import path
from .views import (
    CreateClass, DeleteClass,
)

app_name = 'classes'

urlpatterns = [
    path('create/', CreateClass.as_view(), name='create-class'),
    path('delete/', DeleteClass.as_view(), name='delete-class'),
]
