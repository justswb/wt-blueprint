from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ... import runtime as rt
from ...definition.task import Task

router = APIRouter(prefix='/api/task', tags=['task'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(task: Task):
    rt.assert_project_loaded()
    rt.project.tasks[task.id] = task
    return task.id

@router.get('/{task_id}')
async def get_task(task_id: UUID):
    rt.assert_project_loaded()
    if not task_id in rt.project.tasks.keys():
        raise HTTPException(HTTPStatus.NOT_FOUND, 'No task with id ' + task_id + ' was found')
    return rt.project.tasks[task_id]

@router.post('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def update_task(task_id: UUID, task: Task):
    await get_task(task_id)
    task.id = task_id
    rt.project.tasks[task_id] = task
    return task
