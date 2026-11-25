from http import HTTPStatus

from fastapi import APIRouter

from ...runtime import get_relations, add_relation as _add_relation
from ...definition.relation import Relation

router = APIRouter(prefix='/api/relation', tags=['relation'])


@router.post('/', status_code=HTTPStatus.CREATED)
async def add_relation(relation: Relation):
    _add_relation(relation)
    return get_relations(relation[1])
