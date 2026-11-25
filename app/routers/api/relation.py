from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...definition.relation import Relation, RelationType
from .common import require_project, get_relations

router = APIRouter(prefix='/api/relation', tags=['relation'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def add_relation(relation: Relation):
    project = require_project()
    if relation not in project.relations:
        project.relations.append(relation)
        return get_relations(relation[1])
    raise HTTPException(HTTPStatus.CONFLICT, 'Given relation already exists')


@router.get('/{task_id}')
async def get_relation(task_id: UUID):
    return get_relations(task_id)


@router.delete('/{relation_type}_{task_a_id}_{task_b_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_relation(relation_type: RelationType, task_a_id: UUID, task_b_id: UUID):
    project = require_project()
    idx = project.relations.index((relation_type, task_a_id, task_b_id))
    return require_project().relations.pop(idx)
