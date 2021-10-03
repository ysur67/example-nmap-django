from tasks.models import Task
from rest_framework import viewsets, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.tasks import run_scan_task, stop_task
from rest_framework.decorators import action
from tasks.utils.tools import get_int_value, start_param, length_param
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from tasks.filters import TaskFilter
from tasks.serializers import (TaskListSerializer, TaskDetailSerializer,
                               TaskRunSerializer, TaskCreateSerializer)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TaskFilter


    def create(self, request: Request, *args, **kwargs):
        """Создать задачу на сканирование."""
        response = super().create(request, *args, **kwargs)
        if response.status_code != status.HTTP_201_CREATED:
            return response
        serializer: TaskCreateSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        autostart = serializer.data.get("autostart", False)
        if not autostart:
            return response
        current_task_id = get_int_value(response.data, "id")
        run_scan_task.delay(current_task_id)
        return response

    def update(self, request: Request, *args, **kwargs):
        """Обновить имя и диапазон адресов, если это возможно.

        Обновить задачу невозможно, если она уже выполнена
        или запущена
        """
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
        """Запустить или остановить существующую задачу.

        Задача не может быть запущена дважды, также как и остановлена
        """
        response = {
            "message": str()
        }
        current_task: Task = self.get_object()
        serializer_context = {
            "task": current_task
        }
        serializer: TaskRunSerializer = self.get_serializer(data=request.data,
                                                            context=serializer_context)
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
        if self.action == "create":
            return TaskCreateSerializer
        return super().get_serializer_class()
