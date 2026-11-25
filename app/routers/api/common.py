from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from ...runtime import require_project as _require_project
from ...definition.relation import Relation


def require_project():
    try:
        return _require_project()
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.args)


def get_relations(task_id: UUID) -> list[Relation]:
    return [r for r in require_project().relations if task_id in r]
