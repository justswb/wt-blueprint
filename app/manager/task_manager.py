from uuid import UUID

from ..definition.task import Task
from ..runtime import require_project


def find_task(task_id: UUID) -> tuple[int, Task]:
    for i, t in enumerate(require_project().tasks):
        if t.id == task_id:
            return i, t
    raise LookupError(f'No task with id {task_id} was found')


def create_task(task: Task) -> UUID:
    require_project().tasks.append(task)
    return task.id


def get_task(task_id: UUID) -> tuple[int, Task]:
    return find_task(task_id)
