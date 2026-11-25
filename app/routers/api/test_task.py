from http import HTTPStatus
from uuid import uuid7

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project, find_task
from ...definition.project import Project
from ...definition.task import Task

BASE_URL = 'http://testserver/api/task'
client = TestClient(app, BASE_URL)


TEST_UUID = uuid7()
TEST_TASK_JSON = {
    "id": str(TEST_UUID),
    "name": "test_task_name",
    "desc": "test_task_desc",
    "status": Task.Status.DRAFT.value,
    "relations": {Task.Relation.BLOCKING.value: [str(uuid7())]}
}


def test_create_task():
    load_project(Project(uuid7(), "test_task_proj"))
    response = client.post('/', json=TEST_TASK_JSON)
    assert response.status_code == HTTPStatus.CREATED
    assert find_task(TEST_UUID) is not None
    pass
