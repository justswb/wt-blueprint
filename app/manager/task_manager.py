from uuid import UUID

from ..definition.task import Task
from ..runtime import require_project


def create_task(task: Task) -> UUID:
    require_project().tasks.append(task)
    return task.id
