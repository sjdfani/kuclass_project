from django.contrib import admin
from .models import Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'unit', 'status')
    list_filter = ('status', 'major')


admin.site.register(Lesson, LessonAdmin)
