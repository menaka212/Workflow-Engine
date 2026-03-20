from django.db import models

import uuid
from django.db import models

class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    input_schema = models.JSONField()
    start_step = models.ForeignKey('Step', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Step(models.Model):
    STEP_TYPES = (
        ('task', 'Task'),
        ('approval', 'Approval'),
        ('notification', 'Notification'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    step_type = models.CharField(max_length=20, choices=STEP_TYPES)
    order = models.IntegerField()
    metadata = models.JSONField(blank=True, null=True)

class Rule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='rules')
    condition = models.TextField()
    next_step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    priority = models.IntegerField()    

class Execution(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    workflow_version = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS)
    data = models.JSONField()
    current_step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True)
    logs = models.JSONField(default=list)
    retries = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)