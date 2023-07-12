from django.db import models
from django.utils.translation import ugettext_lazy as _
from major.models import Major


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    major = models.ForeignKey(
        Major, on_delete=models.CASCADE, verbose_name=_('Major'))
    master_name = models.CharField(
        max_length=80, verbose_name=_('Master name'))
    unit = models.IntegerField(_('Unit'), default=0)
    status = models.BooleanField(_('Status'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
