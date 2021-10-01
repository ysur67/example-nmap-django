from djongo import models
from .result import TaskResult
from tasks.utils import keys_to_strings


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
    result = models.JSONField(verbose_name="Результат выполнения задачи",
                              default={})
    status = models.CharField(verbose_name="Текущий статус задачи",
                              choices=Status.choices, max_length=100,
                              default=Status.CREATED)

    @classmethod
    def get_object_by_id(cls, id_: int):
        """Получить инстанс класса по переданнуому id,
        если id не существует будет возвращен `None`

        Args:
            id (int): Ид требуемоего инстанса
        """
        try:
            return cls.objects.get(id=id_)
        except cls.DoesNotExist:
            return None

    @property
    def is_running(self) -> bool:
        return self.status == Status.STARTED

    @property
    def result_is_empty(self) -> bool:
        return self.result is None or self.result == "" or self.result == {}

    def __str__(self) -> str:
        return self.name

    def mark_as_started(self):
        """Пометить задачу, как запущенную."""
        self.status = Status.STARTED
        self.save()

    def mark_as_completed(self):
        """Пометить задачу. как успешно выполненную."""
        self.status = Status.FINISHED
        self.save()

    def set_result(self, new):
        """Установить результат задачи.

        Если задача уже была запущена и ее поле result не пусто,
        то будет поднятно исключание ValueError

        Args:
            new: Новое значение в поле `result`

        Raises:
            ValueError: Задача уже имеет какой-то результат выполнения
        """
        if not self.result_is_empty:
            raise ValueError(f"Task {self.id} has already been started")
        self.result = keys_to_strings(new)
        self.save()
