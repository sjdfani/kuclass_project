from django.urls import path
from .views import (
    CreateLesson, LessonListByMajor, LessonRetrieveUpdateDestroy
)
app_name = 'lessons'

urlpatterns = [
    path('create/', CreateLesson.as_view(), name='create'),
    path('list/<str:major>/', LessonListByMajor.as_view(),
         name='list_by_major'),
    path('<int:pk>/', LessonRetrieveUpdateDestroy.as_view(),
         name='retrieve_update_destroy_lesson'),
]
