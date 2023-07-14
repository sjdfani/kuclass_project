from django.db import models
from users.models import User
from lessons.models import Lesson
from django.utils.translation import ugettext_lazy as _


class RepeatChoose(models.TextChoices):
    ONE = ('one', 'One')
    ALL_WEEKS = ('all_weeks', 'All_weeks')
    SEVERAL = ('several', 'Several')


class Class(models.Model):
    uuid = models.CharField(
        max_length=100, verbose_name=_('Uuid'), unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_(
        'User'), related_name='class_user')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=_(
        'Lesson'), related_name='class_lesson')
    start_time = models.TimeField(verbose_name=_('Start time'))
    end_time = models.TimeField(verbose_name=_('End time'))
    date_of_day = models.DateField(verbose_name=_('Date'))
    status = models.BooleanField(verbose_name=_('Status'))
    repeat = models.CharField(
        max_length=9, choices=RepeatChoose.choices, verbose_name=_('Repeat'))

    def __str__(self) -> str:
        return self.lesson.name
