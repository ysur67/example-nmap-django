from django.core.management.base import BaseCommand, CommandError
from tasks.tasks import run_scan_task


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--task", type=int)

    def handle(self, *args, **options):
        task_id = options["task"]
        run_scan_task.delay(task_id)
