from http import HTTPStatus
from uuid import UUID, uuid7

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project
from ...definition.project import Project
from ...definition.task import Task
from ...definition.feature import Feature
from .common import require_project

client = TestClient(app, 'http://testserver/api/feature')


TEST_TASKS = Task('a'), Task('b')
TEST_FEATURE = Feature('test_feature_name', desc='test_feature_desc', tasks=[TEST_TASKS[0].id])
TEST_FEATURE_JSON = {'name': 'test_feature_name', 'desc': 'test_feature_desc', 'tasks': [str(TEST_TASKS[0].id)]}


def new_test_feature() -> Feature:
    # fresh copy per test: routes mutate feature.tasks in place
    return Feature(TEST_FEATURE.name, TEST_FEATURE.id, TEST_FEATURE.desc, list(TEST_FEATURE.tasks))


def feature_to_dict(f: Feature) -> dict:
    d = vars(f).copy()
    d['id'] = str(f.id)
    d['tasks'] = [str(t) for t in f.tasks]
    return d


def test_create_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS))
    response = client.post('/', json=TEST_FEATURE_JSON)
    assert response.status_code == HTTPStatus.CREATED
    expected = Feature(TEST_FEATURE_JSON['name'], UUID(response.json()), TEST_FEATURE_JSON['desc'], [TEST_TASKS[0].id])
    features = require_project().features
    assert features == [expected]
    pass


def test_create_feature_unknown_task():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS))
    request_json = {**TEST_FEATURE_JSON, 'tasks': [str(uuid7())]}
    response = client.post('/', json=request_json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert require_project().features == []
    pass


def test_get_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.get(f'/{TEST_FEATURE.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == feature_to_dict(TEST_FEATURE)
    pass


def test_get_feature_missing():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS))
    response = client.get(f'/{uuid7()}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    pass


def test_update_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    request_json = {'name': 'mutation_feature_name', 'desc': 'mutation_feature_desc', 'tasks': [str(TEST_TASKS[1].id)]}
    response = client.post(f'/{TEST_FEATURE.id}', json=request_json)
    assert response.status_code == HTTPStatus.ACCEPTED
    expected = Feature(request_json['name'], TEST_FEATURE.id, request_json['desc'], [TEST_TASKS[1].id])
    assert response.json() == feature_to_dict(expected)
    features = require_project().features
    assert features == [expected]
    pass


def test_update_feature_missing():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS))
    response = client.post(f'/{uuid7()}', json=TEST_FEATURE_JSON)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert require_project().features == []
    pass


def test_update_feature_unknown_task():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    request_json = {**TEST_FEATURE_JSON, 'tasks': [str(uuid7())]}
    response = client.post(f'/{TEST_FEATURE.id}', json=request_json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]
    pass


def test_delete_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.delete(f'/{TEST_FEATURE.id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json() == feature_to_dict(TEST_FEATURE)
    assert require_project().features == []
    pass


def test_delete_feature_missing():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.delete(f'/{uuid7()}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert require_project().features == [TEST_FEATURE]
    pass


def test_add_task_to_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.post(f'/{TEST_FEATURE.id}/task/{TEST_TASKS[1].id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    features = require_project().features
    assert response.json() == feature_to_dict(features[0])
    assert features[0].tasks == [TEST_TASKS[0].id, TEST_TASKS[1].id]
    pass


def test_add_task_to_missing_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS))
    response = client.post(f'/{uuid7()}/task/{TEST_TASKS[0].id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    pass


def test_add_unknown_task_to_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.post(f'/{TEST_FEATURE.id}/task/{uuid7()}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]
    pass


def test_add_existing_task_to_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.post(f'/{TEST_FEATURE.id}/task/{TEST_TASKS[0].id}')
    assert response.status_code == HTTPStatus.CONFLICT
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]
    pass


def test_add_same_task_to_two_features():
    features = [Feature('f1'), Feature('f2')]
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], features))
    first = client.post(f'/{features[0].id}/task/{TEST_TASKS[0].id}')
    second = client.post(f'/{features[1].id}/task/{TEST_TASKS[0].id}')
    assert first.status_code == HTTPStatus.ACCEPTED
    assert second.status_code == HTTPStatus.ACCEPTED
    stored = require_project().features
    assert stored[0].tasks == [TEST_TASKS[0].id]
    assert stored[1].tasks == [TEST_TASKS[0].id]
    pass


def test_remove_task_from_feature():
    feature = Feature('test_feature_name', desc='test_feature_desc', tasks=[TEST_TASKS[0].id, TEST_TASKS[1].id])
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [feature]))
    response = client.delete(f'/{feature.id}/task/{TEST_TASKS[0].id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    features = require_project().features
    assert response.json() == feature_to_dict(features[0])
    assert features[0].tasks == [TEST_TASKS[1].id]
    pass


def test_remove_task_from_missing_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS))
    response = client.delete(f'/{uuid7()}/task/{TEST_TASKS[0].id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    pass


def test_remove_task_not_in_feature():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.delete(f'/{TEST_FEATURE.id}/task/{TEST_TASKS[1].id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]
    pass


def test_get_features_by_task():
    features = [
        Feature('f1', tasks=[TEST_TASKS[0].id, TEST_TASKS[1].id]),
        Feature('f2', tasks=[TEST_TASKS[0].id]),
        Feature('f3', tasks=[TEST_TASKS[1].id]),
    ]
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], features))
    response = client.get(f'/task/{TEST_TASKS[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [feature_to_dict(features[0]), feature_to_dict(features[1])]
    pass


def test_get_features_by_task_none():
    load_project(Project(uuid7(), 'test_feature_proj', TEST_TASKS, [], [new_test_feature()]))
    response = client.get(f'/task/{TEST_TASKS[1].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
    pass
