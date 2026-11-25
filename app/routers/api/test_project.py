from http import HTTPStatus
import uuid

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project, require_project
from ...definition.project import Project


BASE_URL = 'http://testserver/api/project'
client = TestClient(app, BASE_URL)


TEST_UUID = uuid.uuid7()
TEST_PROJ_JSON = {"id":str(TEST_UUID),"name":"test_proj_name", "tasks":[]}


def test_create_project(monkeypatch):
    def mockreturn():
        return TEST_UUID
    monkeypatch.setattr(uuid, "uuid7", mockreturn)
    response = client.post('/new', json={"name":TEST_PROJ_JSON["name"]})
    assert response.status_code == HTTPStatus.CREATED.value
    assert response.json() == TEST_PROJ_JSON
    pass


def test_open_project():
    response = client.post('/', json=TEST_PROJ_JSON)
    assert response.status_code == HTTPStatus.OK
    assert require_project().id == TEST_UUID
    pass


def test_require_unloaded_project():
    load_project(Project(uuid.uuid7(), "test_require_unloaded_project_name"))
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    pass
