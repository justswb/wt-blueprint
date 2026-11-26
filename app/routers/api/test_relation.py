from http import HTTPStatus
from uuid import uuid7

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project
from ...definition.project import Project
from ...definition.task import Task
from ...definition.relation import RelationType

client = TestClient(app, 'http://testserver/api/relation')


TEST_TASKS = Task('a'), Task('b')
TEST_RELATION = RelationType.BLOCK, TEST_TASKS[0].id, TEST_TASKS[1].id
TEST_RELATION_JSON = RelationType.BLOCK.value, str(TEST_TASKS[0].id), str(TEST_TASKS[1].id)


def test_add_relation_endpoint():
    load_project(Project(uuid7(), 'test_add_relation_endpoint', TEST_TASKS))
    response = client.post('/', json=TEST_RELATION_JSON)
    assert response.status_code == HTTPStatus.CREATED
    response = client.post('/', json=TEST_RELATION_JSON)
    assert response.status_code == HTTPStatus.CONFLICT


def test_get_relation_endpoint():
    load_project(Project(uuid7(), 'test_get_relation_endpoint', TEST_TASKS, [TEST_RELATION]))
    response = client.get(f'/{TEST_TASKS[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [list(TEST_RELATION_JSON)]


def test_delete_relation_endpoint():
    load_project(Project(uuid7(), 'test_delete_relation_endpoint', TEST_TASKS, [TEST_RELATION]))
    response = client.delete(f'/{RelationType.BLOCK.value}_{TEST_TASKS[0].id}_{TEST_TASKS[1].id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert client.get(f'/{TEST_TASKS[0].id}').json() == []
