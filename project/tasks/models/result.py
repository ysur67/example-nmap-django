from djongo import models


class TaskResult(models.Model):
    """Модель результата выполнения задачи."""
    host = models.CharField(max_length=200)
    hostname = models.CharField(max_length=200)
    hostname_type = models.CharField(max_length=200)
    protocol = models.CharField(max_length=100)
    port = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    extra_info = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    version = models.CharField(max_length=100)
    conf = models.CharField(max_length=50)
    cpe = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.host
