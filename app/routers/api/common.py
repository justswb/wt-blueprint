from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from ...runtime import require_project as _require_project
from ...definition.task import Task
from ...definition.relation import Relation
from ...definition.feature import Feature


def find_task(task_id: UUID) -> tuple[int, Task | None]:
    for i, t in enumerate(require_project().tasks):
        if t.id == task_id:
            return i, t
        pass
    return -1, None


def find_feature(feature_id: UUID) -> tuple[int, Feature | None]:
    for i, f in enumerate(require_project().features):
        if f.id == feature_id:
            return i, f
        pass
    return -1, None


def require_project():
    try:
        return _require_project()
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.args)


def get_relations(task_id: UUID) -> list[Relation]:
    return [r for r in require_project().relations if task_id in r]


def get_features(task_id: UUID) -> list[Feature]:
    return [f for f in require_project().features if task_id in f.tasks]
