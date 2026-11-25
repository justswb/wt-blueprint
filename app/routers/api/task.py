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
    task = next((t for t in require_project().tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'No task with id ' + str(task_id) + ' was found')
    return task

@router.post('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def update_task(task_id: UUID, task: Task):
    task_prev = await get_task(task_id)
    task.id = task_prev.id
    project = require_project()
    project.tasks[project.index(task_prev)] = task
    return task

@router.delete('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_task(task_id: UUID):
    task = await get_task(task_id)
    project = require_project()
    idx = project.tasks.index(task)
    return project.tasks.pop(idx)
