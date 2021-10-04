from rest_framework import serializers
from tasks.models import Task
from tasks.utils import ReadWriteSerializerMethodField, is_ip_range


class TaskBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "status", "ip_range", )
        read_only_fields = ("status", )

    @property
    def task_is_immutable(self) -> bool:
        return self.instance and (self.instance.is_running or self.instance.is_finished)

class TaskListSerializer(TaskBaseSerializer):
    class Meta(TaskBaseSerializer.Meta):
        pass

    def validate(self, attrs):
        if self.task_is_immutable:
            raise serializers.ValidationError(("At the moment task "
                                               "is running or finished and cannot be changed"))
        return attrs


class TaskDetailSerializer(TaskBaseSerializer):
    result = serializers.JSONField(required=False)

    class Meta(TaskBaseSerializer.Meta):
        fields = ("id", "name", "status", "ip_range", "result")


class TaskRunSerializer(serializers.Serializer):
    START_ACTION = "start"
    STOP_ACTION = "stop"

    action = serializers.ChoiceField(choices=(START_ACTION, STOP_ACTION))

    def validate(self, attrs):
        current_task = self.context.get("task", None)
        if current_task is None:
            raise ValueError("There is no current task in context")
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


class TaskCreateSerializer(TaskBaseSerializer):
    autostart = ReadWriteSerializerMethodField("get_autostart_value",
                                               required=False)

    class Meta(TaskBaseSerializer.Meta):
        fields = ("id", "name", "ip_range", "autostart", )

    def get_autostart_value(self, instance) -> bool:
        request = self.context.get("request", None)
        return request.data.get("autostart", False)

    def create(self, validated_data):
        if "autostart" in validated_data.keys():
            validated_data.pop("autostart")
        return super().create(validated_data)

    def validate_autostart(self, attrs):
        value = attrs.get("autostart", None)
        if not isinstance(value, bool):
            raise serializers.ValidationError("Use boolean value")
        return attrs

    def validate_ip_range(self, value):
        if not is_ip_range(value):
            raise serializers.ValidationError("Value is not a valid address range")
        return value
