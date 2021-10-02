from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.tasks import run_scan_task, stop_task
from rest_framework.decorators import action
from tasks.utils.tools import get_int_value


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    UNPROCESSABLE_CODE = 422
    BAD_REQQUEST_CODE = 400

    def list(self, request: Request, *args, **kwargs):
        request_params = request.query_params.copy()
        range_start = get_int_value(request_params, "start")
        MIN_START_RANGE = 0
        if range_start < MIN_START_RANGE:
            range_start = MIN_START_RANGE
        range_size = get_int_value(request_params, "length")
        qs = self.get_queryset()
        if range_start > MIN_START_RANGE:
            qs = qs[range_start - 1:]
        if range_size != 0:
            qs = qs[:range_size]
        return Response(self.get_serializer(qs, many=True).data)

    def create(self, request, *args, **kwargs):
        # Создать объект, как обычно и только потом запускаем задачу
        response = super().create(request, *args, **kwargs)
        if response.status_code != 201:
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
        current_task: Task = self.get_object()
        response = {
            "message": str()
        }
        if current_task.is_running:
            response["message"] = ("At the moment task "
                                   "is running and cannot be changed")
            return Response(response, status=self.UNPROCESSABLE_CODE)
        if current_task.is_finished:
            response["message"] = ("Task has already been finished "
                                   "and cannot be changed")
            return Response(response, self.UNPROCESSABLE_CODE)
        request_data = request.data.copy()
        new_ip_range = request_data.get("ip_range", None)
        new_name = request_data.get("name", None)
        current_task.set_name(new_name)
        current_task.set_ip_range(new_ip_range)
        response["message"] = "The task has been successfully updated"
        return Response(response)

    @action(methods=["post",], detail=True)
    def change_task_state(self, request: Request, *args, **kwargs):
        current_task: Task = self.get_object()
        ACTION_START = "start"
        ACTION_STOP = "stop"
        task_action = request.data.get("action", None)
        response = {
            "message": str()
        }
        # Выходим, если получен неправильный параметр
        if task_action not in (ACTION_START, ACTION_STOP):
            response["message"] = "Action not known"
            return Response(response, self.UNPROCESSABLE_CODE)
        # Выходим, если задача уже выполнена
        if current_task.is_finished:
            response["message"] = "The task has already been finished"
            return Response(response, self.UNPROCESSABLE_CODE)
        # Если задача запущена, пытаемся ее остановить
        if current_task.is_running:
            # Если задачу пытаются повторно запустить - выходим
            if task_action == ACTION_START:
                response["message"] = ("At the moment task is running "
                                   "and cannot be started again")
                return Response(response, self.UNPROCESSABLE_CODE)
            stop_task.delay(current_task.celery_id)
            response["message"] = "The task has been successfully stopped"
            return Response(response)
        # На этом этапе задача не может быть запущена
        # Выходим, если задача уже остановлена и ее пытаются запустить
        if task_action == ACTION_STOP:
            response["message"] = ("The task has been already stopped "
                                   "and cannot be stopped again")
            return Response(response, self.UNPROCESSABLE_CODE)
        # Пытаемся запустить задачу
        if task_action == ACTION_START:
            run_scan_task.delay(current_task.id)
            response["message"] = "The task has been successfully started"
            return Response(response)
        # Отдаем 400 код, если что-то пошло не так
        response["message"] = "Bad request"
        return Response(response, self.BAD_REQQUEST_CODE)
