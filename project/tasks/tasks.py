from project.celery import app
from tasks.models import Task
from tasks.utils import ScanService, NmapService


@app.task
def run_scan_task(task_id: int):
    """Запустить задачу сканирования.

    Args:
        task_id (int): Ид требуемой задачи

    Raises:
        ValueError: Если задача уже была запущена
    """
    current_task: Task = Task.get_object_by_id(task_id)
    if current_task is None:
        return
    if current_task.is_running:
        raise ValueError(f"Task {task_id} is started already")
    current_task.mark_as_started()
    scan_service: ScanService = NmapService(current_task.ip_range)
    # Запускаем задачу с флагом -A
    # aggressive mode
    scan_result = scan_service.scan("-A")
    current_task.set_result(scan_result)
    current_task.mark_as_completed()
