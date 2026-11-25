from typing import Annotated
from uuid import UUID, uuid7
from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ...runtime import load_project, require_project
from ...definition.project import Project

router = APIRouter(prefix='/api/project', tags=['project'])


class CreateProjectReq(BaseModel):
    name: str
    pass


@router.post('/new', status_code=HTTPStatus.CREATED)
async def create_project(req: CreateProjectReq):
    return Project(uuid7(), req.name)

@router.post('/', response_class=RedirectResponse, status_code=HTTPStatus.SEE_OTHER)
async def open_project(req: Project, host: Annotated[str, Header(include_in_schema=False)]):
    load_project(req)
    return 'http://' + host + router.prefix + '/' + str(req.id)

@router.get('/{proj_id}')
async def get_proejct(proj_id: UUID):
    project = require_project()
    if project.id != proj_id:
        raise HTTPException(HTTPStatus.NOT_FOUND, f'No loaded project with id {proj_id} was found')
    return project
