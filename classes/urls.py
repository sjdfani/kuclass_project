from django.urls import path
from .views import (
    CreateClass, DeleteClass, RetrieveUpdateClass, UpdateMultiClass,
    GetAllClassesByUser, GetClassesByUserWithDate,
)

app_name = 'classes'

urlpatterns = [
    path('create/', CreateClass.as_view(), name='create-class'),
    path('delete/', DeleteClass.as_view(), name='delete-class'),
    path('<int:pk>/details/',
         RetrieveUpdateClass.as_view(), name='retrieve-update-class'),
    path('multi-update/<int:pk>/details/<str:repeat>/',
         UpdateMultiClass.as_view(), name='update-multi-class'),
    path('get-classes/', GetAllClassesByUser.as_view(), name="get-classes"),
    path('get-classes/from=<str:from>/to=<str:to>/',
         GetClassesByUserWithDate.as_view(), name="get-classes-by-dates"),
]
