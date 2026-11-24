from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ...definition.project import Project

router = APIRouter(prefix='/api/project', tags=['project'])


class CreateProjectReq(BaseModel):
    name: str
    pass


@router.post('/')
async def create_project(req: CreateProjectReq) -> JSONResponse:
    return Project(req.name)
