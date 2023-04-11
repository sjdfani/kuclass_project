from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class User(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(_('Username'), max_length=50, unique=True)
    email = models.EmailField(_("Email"), unique=True)
    fullname = models.CharField(
        max_length=50, verbose_name=_('Fullname'), null=True, blank=True)
    major = models.CharField(
        max_length=50, verbose_name=_('Major'), null=True, blank=True)
    photo = models.ImageField(
        upload_to='user/photo/', verbose_name=_('Photo'), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class EmailCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('User')
    )
    code = models.CharField(
        max_length=10, verbose_name=_('Code'), null=True, blank=True
    )
    unique_id = models.CharField(
        max_length=100, verbose_name=_('Unique id'), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name=_('Status'))

    def __str__(self) -> str:
        return self.user.email
