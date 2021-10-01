from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


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

    def get_int_value(self, dict_, key):
        DEFAULT_VALUE = 0
        try:
            return int(dict_.get(key, DEFAULT_VALUE))
        except TypeError:
            return DEFAULT_VALUE
