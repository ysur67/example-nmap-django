from django_filters import rest_framework as filters
from tasks.models import Task


class TaskFilter(filters.FilterSet):
    start = filters.NumberFilter(field_name="id", lookup_expr='gte')
    length = filters.NumberFilter(method="limit_qs_size")

    DEFAULT_LENGTH = 0

    class Meta:
        model = Task
        fields = ("start", "length", )

    def limit_qs_size(self, queryset, name, value):
        if value == self.DEFAULT_LENGTH:
            return queryset
        return queryset[:value]
