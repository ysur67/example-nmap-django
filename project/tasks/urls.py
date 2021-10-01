from django.urls import path
from tasks.views import TaskViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register('tasks', TaskViewSet)
urlpatterns = router.urls
