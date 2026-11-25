from http import HTTPStatus
from uuid import uuid7

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project, find_task
from ...definition.project import Project
from ...definition.task import Task

BASE_URL = 'http://testserver/api/task'
client = TestClient(app, BASE_URL)


TEST_TASK = Task("test_task_name", uuid7(), "test_task_desc", Task.Status.DRAFT, {Task.Relation.BLOCKING: [uuid7()]})
def task_to_dict(t: Task) -> dict:
    return {
        "id": str(t.id),
        "name": t.name,
        "desc": t.desc,
        "status": t.status.value,
        "relations": {r.value: list(map(str, t.relations[r])) for r in t.relations.keys()}
    }


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
