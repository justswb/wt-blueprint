from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from ...definition.relation import Relation
from .common import require_project, get_relations

router = APIRouter(prefix='/api/relation', tags=['relation'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def add_relation(relation: Relation):
    project = require_project()
    if relation not in project.relations:
        project.relations.append(relation)
        return get_relations(relation[1])
    raise HTTPException(HTTPStatus.CONFLICT, 'Given relation already exists')
