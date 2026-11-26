from uuid import UUID

from ..definition.feature import Feature
from ..runtime import require_project
from . import task_manager


def require_tasks_exist(task_ids: list[UUID]) -> None:
    for task_id in task_ids:
        task_manager.find_task(task_id)


def create_feature(feature: Feature) -> UUID:
    require_tasks_exist(feature.tasks)
    require_project().features.append(feature)
    return feature.id
