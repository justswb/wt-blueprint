from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ...definition.feature import Feature
from .common import require_project, find_task, find_feature, get_features

router = APIRouter(prefix='/api/feature', tags=['feature'])


def require_tasks_exist(task_ids: list[UUID]):
    for task_id in task_ids:
        _, task = find_task(task_id)
        if task is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, f'No task with id {task_id} was found')
        pass
    pass


def require_feature(feature_id: UUID) -> tuple[int, Feature]:
    idx, feature = find_feature(feature_id)
    if feature is not None:
        return idx, feature
    raise HTTPException(HTTPStatus.NOT_FOUND, f'No feature with id {feature_id} was found')


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_feature(feature: Feature):
    require_tasks_exist(feature.tasks)
    require_project().features.append(feature)
    return feature.id


@router.get('/task/{task_id}')
async def get_features_by_task(task_id: UUID):
    return get_features(task_id)


@router.get('/{feature_id}')
async def get_feature(feature_id: UUID):
    _, feature = require_feature(feature_id)
    return feature


@router.post('/{feature_id}', status_code=HTTPStatus.ACCEPTED)
async def update_feature(feature_id: UUID, feature: Feature):
    idx, feature_prev = require_feature(feature_id)
    require_tasks_exist(feature.tasks)
    feature.id = feature_prev.id
    require_project().features[idx] = feature
    return feature


@router.delete('/{feature_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_feature(feature_id: UUID):
    idx, _ = require_feature(feature_id)
    return require_project().features.pop(idx)


@router.post('/{feature_id}/task/{task_id}', status_code=HTTPStatus.CREATED)
async def add_task_to_feature(feature_id: UUID, task_id: UUID):
    _, feature = require_feature(feature_id)
    require_tasks_exist([task_id])
    if task_id in feature.tasks:
        raise HTTPException(HTTPStatus.CONFLICT, f'Task {task_id} is already in feature {feature_id}')
    feature.tasks.append(task_id)
    return feature


@router.delete('/{feature_id}/task/{task_id}', status_code=HTTPStatus.ACCEPTED)
async def remove_task_from_feature(feature_id: UUID, task_id: UUID):
    _, feature = require_feature(feature_id)
    if task_id not in feature.tasks:
        raise HTTPException(HTTPStatus.NOT_FOUND, f'No task with id {task_id} was found in feature {feature_id}')
    feature.tasks.remove(task_id)
    return feature
