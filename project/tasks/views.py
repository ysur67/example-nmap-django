from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.tasks import run_scan_task


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def list(self, request: Request, *args, **kwargs):
        request_params = request.query_params.copy()
        range_start = self.get_int_value(request_params, "start")
        if range_start < 0:
            range_start = 0
        range_size = self.get_int_value(request_params, "length")
        qs = self.get_queryset()
        if range_start != 0 and range_start != 1:
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
        current_task_id = self.get_int_value(response.data, "id")
        run_scan_task.delay(current_task_id)
        return response

    def update(self, request: Request, *args, **kwargs):
        current_task: Task = self.get_object()
        response = {
            "message": str()
        }
        BAD_REQUEST_CODE = 422
        if current_task.is_running:
            response["message"] = ("At the moment task "
                                   "is running and cannot be changed")
            return Response(response, status=BAD_REQUEST_CODE)
        if current_task.is_finished:
            response["message"] = ("Task has already been finished "
                                   "and cannot be changed")
            return Response(response, BAD_REQUEST_CODE)
        request_data = request.data.copy()
        new_ip_range = request_data.get("ip_range", None)
        new_name = request_data.get("name", None)
        current_task.set_name(new_name)
        current_task.set_ip_range(new_ip_range)
        response["message"] = "The task has been successfully updated"
        return Response(response)

    def get_int_value(self, dict_, key):
        DEFAULT_VALUE = 0
        try:
            return int(dict_.get(key, DEFAULT_VALUE))
        except TypeError:
            return DEFAULT_VALUE
