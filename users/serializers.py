from rest_framework import serializers
from .models import User, EmailCode
from .utils import number_generator
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['username'].find('@') != -1:
            raise serializers.ValidationError(
                {'message': 'you can not use @ in username'}
            )
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {'message': 'this username is taken'}
            )
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {'message': 'this email is taken.'}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        if attrs['username_or_email'].find('@') != -1 and attrs['username_or_email'].find('.com') != -1:
            if not User.objects.filter(email=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        else:
            if not User.objects.filter(username=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()

    def validate(self, attrs):
        if attrs['username_or_email'].find('@') != -1 and attrs['username_or_email'].find('.com') != -1:
            if not User.objects.filter(email=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        else:
            if not User.objects.filter(username=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        return attrs

    def get_user(self, username_or_email: str):
        if username_or_email.find('@') != -1 and username_or_email.find('.com') != -1:
            return User.objects.get(email=username_or_email)
        return User.objects.get(username=username_or_email)

    def process(self, user):
        code = number_generator(5)
        obj = EmailCode.objects.get_or_create(user=user)[0]
        obj.code = code
        obj.unique_id = uuid.uuid4().hex
        obj.status = True
        obj.save()
        return obj.unique_id

    def save(self, **kwargs):
        username_or_email = self.validated_data['username_or_email']
        user = self.get_user(username_or_email)
        return self.process(user)


class VerifyForgotPasswordSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    unique_id = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        if attrs['username_or_email'].find('@') != -1 and attrs['username_or_email'].find('.com') != -1:
            if not User.objects.filter(email=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        else:
            if not User.objects.filter(username=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        if not EmailCode.objects.filter(unique_id=attrs['unique_id'], status=True).exists():
            raise serializers.ValidationError(
                {'message': 'your unique id not found or your code was expired'}
            )
        return attrs

    def get_user(self, username_or_email: str):
        if username_or_email.find('@') != -1 and username_or_email.find('.com') != -1:
            return User.objects.get(email=username_or_email)
        return User.objects.get(username=username_or_email)

    def process(self, user: User, unique_id: str, code: str):
        obj = EmailCode.objects.filter(
            user=user, unique_id=unique_id, status=True).first()
        if obj:
            if code == obj.code:
                return (True, {'message': 'Your input code is correct'})
            else:
                return (False, {'message': 'Your input code is invalid'})
        else:
            return (False, {'message': 'Your code was expired'})

    def save(self, **kwargs):
        username_or_email = self.validated_data['username_or_email']
        code = self.validated_data['code']
        unique_id = self.validated_data['unique_id']
        user = self.get_user(username_or_email)
        return self.process(user, unique_id, code)


class ConfirmForgetPasswordSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    unique_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['username_or_email'].find('@') != -1 and attrs['username_or_email'].find('.com') != -1:
            if not User.objects.filter(email=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        else:
            if not User.objects.filter(username=attrs['username_or_email']).exists():
                raise serializers.ValidationError(
                    {'message': 'this username or email is not exists'}
                )
        if not EmailCode.objects.filter(unique_id=attrs['unique_id'], status=True).exists():
            raise serializers.ValidationError(
                {'message': 'your unique id not found or your code was expired'}
            )
        return attrs

    def get_user(self, username_or_email: str):
        if username_or_email.find('@') != -1 and username_or_email.find('.com') != -1:
            return User.objects.get(email=username_or_email)
        return User.objects.get(username=username_or_email)

    def process(self, user: User, unique_id: str, password: str):
        obj = EmailCode.objects.filter(
            user=user, unique_id=unique_id, status=True).first()
        if obj:
            user.set_password(password)
            user.save()
            return (True, {'message': 'Your password has been changed'})
        else:
            return (False, {'message': 'Your code was expired'})

    def save(self, **kwargs):
        username_or_email = self.validated_data['username_or_email']
        password = self.validated_data['password']
        unique_id = self.validated_data['unique_id']
        user = self.get_user(username_or_email)
        self.process(user, unique_id, password)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(
                {'message': 'your old password is incorrect'}
            )
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {'message': 'your input passwords are not match'}
            )
        return attrs

    def process(self, user: User, password: str):
        user.set_password(password)
        user.save()

    def save(self, **kwargs):
        password = self.validated_data['password1']
        self.process(self.context['request'].user, password)
