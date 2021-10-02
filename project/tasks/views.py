from tasks.models import Task
from tasks.serializers import TaskListSerializer, TaskDetailSerializer, TaskRunSerializer
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.tasks import run_scan_task, stop_task
from rest_framework.decorators import action
from tasks.utils.tools import get_int_value

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()

    def list(self, request: Request, *args, **kwargs):
        request_params = request.query_params.copy()
        range_start = get_int_value(request_params, "start")
        MIN_START_RANGE = 0
        RANGE_SIZE_DEFAULT_VALUE = 0
        if range_start < MIN_START_RANGE:
            range_start = MIN_START_RANGE
        range_size = get_int_value(request_params, "length")
        qs = self.get_queryset().order_by("id")
        if range_start > MIN_START_RANGE:
            qs = qs.filter(id__gte=range_start)
        if range_size != RANGE_SIZE_DEFAULT_VALUE:
            qs = qs[:range_size]
        return Response(self.get_serializer(qs, many=True).data)

    def create(self, request, *args, **kwargs):
        # Создать объект, как обычно и только потом запускаем задачу
        response = super().create(request, *args, **kwargs)
        if response.status_code != status.HTTP_201_CREATED:
            return response
        autostart = self.request.data.get("autostart", False)
        if not autostart:
            return response
        if not isinstance(autostart, bool):
            return response
        current_task_id = get_int_value(response.data, "id")
        run_scan_task.delay(current_task_id)
        return response

    def update(self, request: Request, *args, **kwargs):
        response = {
            "message": str()
        }
        current_task: Task = self.get_object()
        serializer: TaskListSerializer = self.get_serializer(data=request.data)
        serializer.instance = current_task
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response["message"] = "The task has been successfully updated"
        return Response(response)

    @action(methods=["post",], detail=True)
    def change_task_state(self, request: Request, *args, **kwargs):
        response = {
            "message": str()
        }
        current_task: Task = self.get_object()
        serializer: TaskRunSerializer = self.get_serializer(data=request.data)
        serializer.instance = current_task
        serializer.is_valid(raise_exception=True)
        task_action = serializer.data.get("action", None)
        if current_task.is_running and task_action == TaskRunSerializer.STOP_ACTION:
            stop_task.delay(current_task.celery_id)
            response["message"] = "The task has been successfully stopped"
            return Response(response)
        if not current_task.is_running and task_action == TaskRunSerializer.START_ACTION:
            run_scan_task.delay(current_task.id)
            response["message"] = "The task has been successfully started"
            return Response(response)
        response["message"] = "Bad request"
        return Response(response, status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaskDetailSerializer
        if self.action == "change_task_state":
            return TaskRunSerializer
        return super().get_serializer_class()
