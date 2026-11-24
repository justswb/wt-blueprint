from http import HTTPStatus

from fastapi import APIRouter

from ... import runtime as rt
from ...definition.task import Task

router = APIRouter(prefix='/api/task', tags=['task'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_task(task: Task):
    rt.assert_project_loaded()
    rt.project.tasks.append(task)
    return task.id
