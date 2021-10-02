from rest_framework import serializers
from tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "name", "status", "ip_range")
        read_only_fields = ("status", )

    def validate(self, attrs):
        if self.instance.is_running or self.instance.is_finished:
            raise serializers.ValidationError(("At the moment task "
                                               "is running or finished and cannot be changed"))
        return attrs


class TaskDetailSerializer(serializers.ModelSerializer):
    result = serializers.JSONField(required=False)

    class Meta:
        model = Task
        fields = ("id", "name", "status", "ip_range", "result")
        read_only_fields = ("status", )


class TaskRunSerializer(TaskListSerializer):
    START_ACTION = "start"
    STOP_ACTION = "stop"

    action = serializers.ChoiceField(choices=(START_ACTION, STOP_ACTION))

    class Meta:
        model = Task
        fields = ("action", )
        read_only_fields = ("name", )

    def validate(self, attrs):
        current_task: Task = self.instance
        action = attrs["action"]
        if current_task.is_finished:
            raise serializers.ValidationError("The task has already been finished")
        if current_task.is_running and action == self.START_ACTION:
            raise serializers.ValidationError(("At the moment task is running "
                                               "and cannot be started again"))
        if current_task.is_stopped and action == self.STOP_ACTION:
            raise serializers.ValidationError(("The task has been already stopped "
                                               "and cannot be stopped again"))
        return attrs
