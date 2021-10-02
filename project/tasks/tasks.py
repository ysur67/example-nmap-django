from project.celery import app
from tasks.models import Task
from tasks.utils import ScanService, NmapService
from celery.contrib.abortable import AbortableTask, AbortableAsyncResult


@app.task(bind=True, base=AbortableTask)
def run_scan_task(self, task_id: int):
    """Запустить задачу сканирования.

    Args:
        task_id (int): Ид требуемой задачи

    Raises:
        ValueError: Если задача уже была запущена
    """
    current_task: Task = Task.get_object_by_id(task_id)
    if current_task is None:
        return
    if current_task.is_running or current_task.is_finished:
        raise ValueError(f"Task {task_id} is started or finished already")
    current_task.mark_as_started()
    scan_service: ScanService = NmapService(current_task.ip_range)
    # Запускаем задачу с флагом -A
    # aggressive mode
    scan_result = scan_service.scan("-A")
    current_task.set_result(scan_result)
    current_task.mark_as_completed()

@app.task()
def stop_task(abortable_task_id):
    """Остановить Celery задачу по переданному идентификатору.

    Args:
        abortable_task_id: Идентификатор задачи
    """
    abortable_task = AbortableAsyncResult(abortable_task_id)
    if abortable_task.is_aborted():
        return
    abortable_task.abort()
