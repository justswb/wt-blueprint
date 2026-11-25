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
    response = client.post('/', json=task_to_dict(TEST_TASK))
    assert response.status_code == HTTPStatus.CREATED
    assert find_task(TEST_TASK.id) is not None
    pass
