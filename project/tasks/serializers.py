from rest_framework import serializers
from tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "name", "status", "ip_range")


class TaskDetailSerializer(serializers.ModelSerializer):
    result = serializers.JSONField(required=False)

    class Meta:
        model = Task
        fields = ("id", "name", "status", "ip_range", "result")
