from contextlib import contextmanager
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...definition.feature import Feature
from ...manager import feature_manager
from .common import require_project

router = APIRouter(prefix='/api/feature', tags=['feature'])


@contextmanager
def manager_errors():
    try:
        yield
    except LookupError as exc:
        raise HTTPException(HTTPStatus.NOT_FOUND, str(exc))
    except ValueError as exc:
        raise HTTPException(HTTPStatus.CONFLICT, str(exc))


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_feature(feature: Feature):
    require_project()
    with manager_errors():
        return feature_manager.create_feature(feature)


@router.get('/task/{task_id}')
async def get_features_by_task(task_id: UUID):
    require_project()
    return feature_manager.get_features_by_task(task_id)


@router.get('/{feature_id}')
async def get_feature(feature_id: UUID):
    require_project()
    with manager_errors():
        return feature_manager.get_feature(feature_id)


@router.post('/{feature_id}', status_code=HTTPStatus.ACCEPTED)
async def update_feature(feature_id: UUID, feature: Feature):
    require_project()
    with manager_errors():
        return feature_manager.update_feature(feature_id, feature)


@router.delete('/{feature_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_feature(feature_id: UUID):
    require_project()
    with manager_errors():
        return feature_manager.delete_feature(feature_id)


@router.post('/{feature_id}/task/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def add_task_to_feature(feature_id: UUID, task_id: UUID):
    require_project()
    with manager_errors():
        return feature_manager.add_task_to_feature(feature_id, task_id)


@router.delete('/{feature_id}/task/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def remove_task_from_feature(feature_id: UUID, task_id: UUID):
    require_project()
    with manager_errors():
        return feature_manager.remove_task_from_feature(feature_id, task_id)
