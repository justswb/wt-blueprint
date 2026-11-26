from typing import Annotated
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ...definition.project import Project
from ...manager import project_manager
from .common import require_project

router = APIRouter(prefix='/api/project', tags=['project'])

UUID = uuid.UUID


class CreateProjectReq(BaseModel):
    name: str
    repo: str | None = None
    pass


@router.post('/new', status_code=HTTPStatus.CREATED)
async def create_project(req: CreateProjectReq):
    return project_manager.create_project(req.name, repo=req.repo)

@router.post('/', response_class=RedirectResponse, status_code=HTTPStatus.SEE_OTHER)
async def open_project(req: Project, host: Annotated[str, Header(include_in_schema=False)]):
    project_manager.open_project(req)
    return f'http://{host}{router.prefix}/{req.id}'

@router.get('/{proj_id}')
async def get_project(proj_id: UUID):
    project = require_project()
    if project.id != proj_id:
        raise HTTPException(HTTPStatus.NOT_FOUND, f'No loaded project with id {proj_id} was found')
    return project
