from django.urls import path
from tasks.views import TaskViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path("tasks/<pk>/",
         TaskViewSet.as_view({
             "get": "retrieve",
             "post": "change_task_state",
             "delete": "destroy"}),
         name="get-task"),
]

urlpatterns += router.urls
