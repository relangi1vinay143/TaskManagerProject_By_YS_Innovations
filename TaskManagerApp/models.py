from django.db import models

class TaskModel(models.Model):
    id = models.AutoField(primary_key=True)
    task_title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    created_date = models.DateField()

