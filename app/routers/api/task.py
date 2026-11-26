from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...definition.task import Task
from ...definition.git_ref import GitRef
from .common import require_project, find_task

router = APIRouter(prefix='/api/task', tags=['task'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(task: Task):
    require_project().tasks.append(task)
    return task.id

@router.get('/{task_id}')
async def get_task(task_id: UUID):
    idx, task = find_task(task_id)
    if task is not None:
        return idx, task
    raise HTTPException(HTTPStatus.NOT_FOUND, f'No task with id {task_id} was found')

@router.post('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def update_task(task_id: UUID, task: Task):
    idx, task_prev = await get_task(task_id)
    if task_prev.status == Task.Status.DONE:
        if task.status == Task.Status.DONE:
            raise HTTPException(HTTPStatus.FORBIDDEN, 'Cannot update done task')
        task.ref = GitRef(task.ref.branch, None, None)
        pass
    task.id = task_prev.id
    require_project().tasks[idx] = task
    return task

@router.delete('/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_task(task_id: UUID):
    idx, _ = await get_task(task_id)
    project = require_project()
    task = project.tasks.pop(idx)
    project.relations[:] = [r for r in project.relations if task_id not in r]
    for feature in project.features:
        feature.tasks[:] = [t for t in feature.tasks if t != task_id]
    return task
