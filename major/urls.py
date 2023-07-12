from django.urls import path
from .views import (
    CreateMajor,
)

app_name = 'major'

urlpatterns = [
    path('create/', CreateMajor.as_view(), name='create'),
]
