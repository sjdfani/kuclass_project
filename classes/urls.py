from django.urls import path
from .views import (
    CreateClass,
)

app_name = 'classes'

urlpatterns = [
    path('create/', CreateClass.as_view(), name='create'),
]
