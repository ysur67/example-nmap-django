from django.urls import path
from tasks.views import TaskViewSet


list_paths = TaskViewSet.as_view({
    "get": "list",
    "post": "create"
})
detail_paths = TaskViewSet.as_view({
    "get": "retrieve",
    "post": "change_task_state",
    "put": "update",
    "delete": "destroy"
})

urlpatterns = [
    path("tasks/", list_paths, name="task-list"),
    path("task/<int:pk>/", detail_paths, name="task-detail")
]
