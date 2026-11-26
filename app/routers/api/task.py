from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...definition.task import Task
from ...definition.git_ref import GitRef
from ...manager import task_manager
from .common import require_project

router = APIRouter(prefix='/api/task', tags=['task'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(task: Task):
    require_project()
    return task_manager.create_task(task)

@router.get('/{task_id}')
async def get_task(task_id: UUID):
    require_project()
    try:
        return task_manager.get_task(task_id)
    except LookupError as exc:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(exc))

@router.post('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def update_task(task_id: UUID, task: Task):
    require_project()
    try:
        return task_manager.update_task(task_id, task)
    except LookupError as exc:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(exc))
    except PermissionError as exc:
        raise HTTPException(HTTPStatus.FORBIDDEN, str(exc))

@router.delete('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_task(task_id: UUID):
    require_project()
    try:
        return task_manager.delete_task(task_id)
    except LookupError as exc:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(exc))
