from django.db import models


class Status(models.TextChoices):
    """Статусы выполнения задачи."""
    CREATED = "created", "Создан"
    STARTED = "started", "Запущен"
    STOPPED = "stopped", "Остановлен"
    FINISHED = "finished", "Выполнен"


class Task(models.Model):
    """Модель задачи на сканирование."""
    name = models.CharField(verbose_name="Наименование задачи",
                            max_length=200)
    ip_range = models.CharField(verbose_name="Диапазон адресов",
                                max_length=200)
    result = models.TextField(verbose_name="Результат работы задачи")
    status = models.CharField(verbose_name="Текущий статус задачи",
                              choices=Status.choices, max_length=100,
                              default=Status.CREATED)

    def __str__(self) -> str:
        return self.name
