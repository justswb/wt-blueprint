from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ... import runtime as rt
from ...definition.task import Task

router = APIRouter(prefix='/api/task', tags=['task'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(task: Task):
    rt.assert_project_loaded()
    rt.project.tasks.append(task)
    return task.id

@router.get('/{task_id}')
async def get_task(task_id: UUID):
    rt.assert_project_loaded()
    task = next((t for t in rt.project.tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'No task with id ' + str(task_id) + ' was found')
    return task

@router.post('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def update_task(task_id: UUID, task: Task):
    task_prev = await get_task(task_id)
    task.id = task_prev.id
    rt.project.tasks[task_id] = task
    return task

@router.delete('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_task(task_id: UUID):
    task = await get_task(task_id)
    idx = rt.project.tasks.index(task)
    return rt.project.tasks.pop(idx)
