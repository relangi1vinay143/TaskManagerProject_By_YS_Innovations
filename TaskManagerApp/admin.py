from django.contrib import admin
from TaskManagerApp.models import TaskModel
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_title', 'description', 'status', 'created_date']
admin.site.register(TaskModel,TaskAdmin)