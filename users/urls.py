from django.urls import path
from .views import (
    Register, Login, ForgotPassword, VerifyForgotPassword, ConfirmForgotPassword,
    ChangePassword,
)

app_name = 'users'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('verify-forgot-password/', VerifyForgotPassword.as_view(),
         name='verify_forgot_password'),
    path('confirm-forgot-password/', ConfirmForgotPassword.as_view(),
         name='confirm_forgot_password'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]
