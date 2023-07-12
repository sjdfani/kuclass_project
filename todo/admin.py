from django.contrib import admin
from .models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = ('user', 'end_at', 'complete_date', 'state')
    list_filter = ('state',)
    list_editable = ('state',)


admin.site.register(Job, JobAdmin)
