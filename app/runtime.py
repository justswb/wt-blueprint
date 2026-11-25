from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from .definition.project import Project
from .definition.task import Task

_project: Project | None = None

def load_project(target: Project) -> None:
    # if _project is not None: # confirm or autosave
    global _project
    _project = target
    pass

def require_project() -> Project:
    if _project is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='No project loaded')
    return _project

def find_task(task_id: UUID) -> tuple[int, Task | None]:
    for i, t in enumerate(require_project().tasks):
        if t.id == task_id:
            return i, t
        pass
    return None
