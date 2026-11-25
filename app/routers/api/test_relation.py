from http import HTTPStatus
from uuid import uuid7

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project, get_relations
from ...definition.project import Project
from ...definition.task import Task
from ...definition.relation import RelationType

client = TestClient(app, 'http://testserver/api/relation')


TEST_TASKS = Task('a'), Task('b')


def test_add_relation():
    load_project(Project(uuid7(), 'test_add_relation', TEST_TASKS))
    response = client.post('/', json=[RelationType.BLOCK.value] + list(map(lambda t: str(t.id), TEST_TASKS)))
    assert response.status_code == HTTPStatus.CREATED
    assert [RelationType.BLOCK] + list(map(lambda t: t.id, TEST_TASKS)) in get_relations()
    pass
