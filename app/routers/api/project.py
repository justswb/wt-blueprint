from typing import Annotated
from uuid import UUID, uuid7
from http import HTTPStatus

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ... import runtime as rt
from ...definition.project import Project

router = APIRouter(prefix='/api/project', tags=['project'])


class CreateProjectReq(BaseModel):
    name: str
    pass

class OpenProjectReq(BaseModel):
    name: str
    id: UUID
    pass


@router.post('/new', status_code=HTTPStatus.CREATED)
async def create_project(req: CreateProjectReq):
    return Project(uuid7(), req.name)

@router.post('/', response_class=RedirectResponse, status_code=HTTPStatus.SEE_OTHER)
async def open_project(req: OpenProjectReq, host: Annotated[str, Header(include_in_schema=False)]):
    # if rt.project is not None: confirm or autosave
    rt.project = Project(req.id, req.name)
    return 'http://' + host + router.prefix + '/' + rt.project.id

@router.get('/{proj_id}')
async def open_proejct(proj_id: str):
    rt.assert_project_loaded()
    if rt.project.id != proj_id:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'No loaded project with id ' + proj_id + ' was found')
    return rt.project
