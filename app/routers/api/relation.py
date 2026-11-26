from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...definition.relation import Relation, RelationType
from ...manager import relation_manager
from .common import require_project

router = APIRouter(prefix='/api/relation', tags=['relation'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def add_relation(relation: Relation):
    require_project()
    try:
        return relation_manager.add_relation(relation)
    except ValueError:
        raise HTTPException(HTTPStatus.CONFLICT, 'Given relation already exists')


@router.get('/{task_id}')
async def get_relation(task_id: UUID):
    require_project()
    return relation_manager.get_relations(task_id)


@router.delete('/{relation_type}_{task_a_id}_{task_b_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_relation(relation_type: RelationType, task_a_id: UUID, task_b_id: UUID):
    require_project()
    return relation_manager.delete_relation((relation_type, task_a_id, task_b_id))
