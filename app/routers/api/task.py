from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...runtime import require_project
from ...definition.task import Task

router = APIRouter(prefix='/api/task', tags=['task'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(task: Task):
    require_project().tasks.append(task)
    return task.id

@router.get('/{task_id}')
async def get_task(task_id: UUID):
    for i, t in enumerate(require_project().tasks):
        if t.id == task_id:
            return i, t
        pass
    raise HTTPException(HTTPStatus.NOT_FOUND, 'No task with id ' + str(task_id) + ' was found')

@router.post('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def update_task(task_id: UUID, task: Task):
    idx, task_prev = await get_task(task_id)
    task.id = task_prev.id
    require_project().tasks[idx] = task
    return task

@router.delete('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_task(task_id: UUID):
    idx, task = await get_task(task_id)
    return require_project().tasks.pop(idx)
