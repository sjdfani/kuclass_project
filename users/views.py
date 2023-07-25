from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .utils import get_tokens_for_user
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, ForgotPasswordSerializer,
    VerifyForgotPasswordSerializer, ConfirmForgetPasswordSerializer, ChangePasswordSerializer,
)


class Register(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            username_or_email = serializer.validated_data['username_or_email']
            password = serializer.validated_data['password']

            if username_or_email.find('@') != -1 and username_or_email.find('.com') != -1:
                user = User.objects.get(email=username_or_email)
            else:
                user = User.objects.get(username=username_or_email)

            if user.check_password(password):
                message = {
                    'user': UserSerializer(user).data,
                    'tokens': get_tokens_for_user(user),
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                message = {'message': 'password is incorrect'}
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPassword(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            code = serializer.save()
            message = {
                'user': serializer.data,
                'code': code,
            }
            return Response(message, status=status.HTTP_200_OK)


class VerifyForgotPassword(APIView):
    def post(self, request):
        serializer = VerifyForgotPasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            state, message = serializer.save()
            if state:
                return Response(message, status=status.HTTP_200_OK)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ConfirmForgotPassword(APIView):
    def post(self, request):
        serializer = ConfirmForgetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            state, message = serializer.save()
            if state:
                return Response(message, status=status.HTTP_200_OK)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
