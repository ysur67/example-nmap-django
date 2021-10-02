from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "ip_range", "status", )
    readonly_fields = ("result", "status", )
    exclude = ("celery_id", )
