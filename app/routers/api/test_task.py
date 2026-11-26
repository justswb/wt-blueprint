from http import HTTPStatus
from uuid import uuid7

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project
from ...definition.project import Project
from ...definition.task import Task
from ...definition.relation import RelationType
from .common import find_task, get_relations

client = TestClient(app, 'http://testserver/api/task')


TEST_TASK = Task("test_task_name", uuid7(), "test_task_desc", Task.Status.DRAFT)
def task_to_dict(t: Task) -> dict:
    d = vars(t).copy()
    d['id'] = str(t.id)
    d['status'] = t.status.value
    return d


def test_create_task():
    load_project(Project(uuid7(), "test_task_proj"))
    request_json = {k: v for k, v in task_to_dict(TEST_TASK).items() if k != 'id'}
    response = client.post('/', json=request_json)
    assert response.status_code == HTTPStatus.CREATED
    assert find_task(TEST_TASK.id) is not None
    pass


def test_get_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    response = client.get(f'/{TEST_TASK.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [0, task_to_dict(TEST_TASK)]
    pass


def test_update_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    request_json = {k: v for k, v in task_to_dict(TEST_TASK).items() if k != 'id'}
    request_json['name'] = 'mutation_task_name'
    response = client.post(f'/{TEST_TASK.id}', json=request_json)
    assert response.status_code == HTTPStatus.ACCEPTED
    assert find_task(TEST_TASK.id)[1].name == request_json['name']
    pass


def test_delete_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    response = client.delete(f'/{TEST_TASK.id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert find_task(TEST_TASK.id) == (-1, None)
    pass


def test_delete_task_removes_relations():
    a = Task('a')
    b = Task('b')
    c = Task('c')
    relation_bc = (RelationType.BLOCK, b.id, c.id)
    load_project(Project(uuid7(), "test_task_proj", [a, b, c], [
        (RelationType.BLOCK, a.id, b.id),
        (RelationType.BLOCK, c.id, a.id),
        relation_bc,
    ]))
    response = client.delete(f'/{a.id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert get_relations(a.id) == []
    assert relation_bc in get_relations(b.id)
    pass
