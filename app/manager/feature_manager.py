from uuid import UUID

from ..definition.feature import Feature
from ..runtime import require_project
from . import task_manager


def find_feature(feature_id: UUID) -> tuple[int, Feature]:
    for i, f in enumerate(require_project().features):
        if f.id == feature_id:
            return i, f
    raise LookupError(f'No feature with id {feature_id} was found')


def get_feature(feature_id: UUID) -> Feature:
    _, feature = find_feature(feature_id)
    return feature


def get_features_by_task(task_id: UUID) -> list[Feature]:
    return [f for f in require_project().features if task_id in f.tasks]


def update_feature(feature_id: UUID, feature: Feature) -> Feature:
    idx, feature_prev = find_feature(feature_id)
    require_tasks_exist(feature.tasks)
    feature.id = feature_prev.id
    require_project().features[idx] = feature
    return feature


def require_tasks_exist(task_ids: list[UUID]) -> None:
    for task_id in task_ids:
        task_manager.find_task(task_id)


def create_feature(feature: Feature) -> UUID:
    require_tasks_exist(feature.tasks)
    require_project().features.append(feature)
    return feature.id
