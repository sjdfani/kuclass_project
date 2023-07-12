from django.db import models
from users.models import User
from django.utils.translation import ugettext_lazy as _


class JobState(models.TextChoices):
    DONE = ('done', 'Done')
    FAILED = ('failed', 'Failed')
    PENDING = ('pending', 'Pending')


class Job(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('User')
    )
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    description = models.TextField(
        verbose_name=_('Description'), null=True, blank=True)
    end_at = models.DateTimeField(verbose_name=_('End at'))
    complete_date = models.DateTimeField(
        verbose_name=_('Complete Date'), null=True, blank=True)
    state = models.CharField(
        max_length=10, verbose_name=_('State'), choices=JobState.choices, default=JobState.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email
