from django.db import models
from django.utils.translation import ugettext_lazy as _


class GradeState(models.TextChoices):
    BACHELOR = ('bachelor', 'Bachelor')
    MASTER = ('master', 'Master')
    PHD = ('phd', 'PhD')


class Major(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    status = models.BooleanField(_('Status'), default=True)
    grade = models.CharField(
        max_length=8, choices=GradeState.choices, verbose_name=_('Grade'))
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
