from rest_framework_simplejwt.tokens import RefreshToken
import string
import random


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def number_generator(size=10):
    chars = string.digits
    return ''.join(random.choice(chars) for _ in range(size))
