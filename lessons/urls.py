from django.urls import path
from .views import (
    CreateLesson,
)
app_name = 'lessons'

urlpatterns = [
    path('create/', CreateLesson.as_view(), name='create')
]
