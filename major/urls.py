from django.urls import path
from .views import (
    CreateMajor, MajorNameList,
)

app_name = 'major'

urlpatterns = [
    path('create/', CreateMajor.as_view(), name='create'),
    path('list/<grade:str>/', MajorNameList.as_view(), name='list'),
]
