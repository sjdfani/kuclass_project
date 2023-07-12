from django.contrib import admin
from .models import Major


class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'status')
    list_filter = ('grade', 'status')


admin.site.register(Major, MajorAdmin)
