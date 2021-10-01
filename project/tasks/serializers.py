from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    result = serializers.JSONField()

    class Meta:
        model = Task
        fields = "__all__"
