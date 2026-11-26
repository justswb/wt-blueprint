from http import HTTPStatus
import uuid

from fastapi.testclient import TestClient

from ...main import app
from ... import runtime
from ...definition.project import Project


client = TestClient(app, 'http://testserver/api/project')


TEST_UUID = uuid.uuid7()
TEST_PROJ_JSON = {"id":str(TEST_UUID),"name":"test_proj_name", "tasks":[], "relations": [], "features": [], "repo": None}


def test_create_project_returns_201():
    response = client.post('/new', json={"name":TEST_PROJ_JSON["name"]})
    assert response.status_code == HTTPStatus.CREATED.value


def test_open_project_redirects():
    response = client.post('/', json=TEST_PROJ_JSON)
    assert response.status_code == HTTPStatus.OK


def test_require_unloaded_project():
    runtime.load_project(Project(uuid.uuid7(), "test_require_unloaded_project_name"))
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    pass


def test_get_project_loaded_returns_200(monkeypatch):
    monkeypatch.setattr(runtime, "_project", None)
    runtime.load_project(Project(TEST_UUID, "test_proj_name"))
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.OK


def test_get_project_when_none_loaded_returns_400(monkeypatch):
    monkeypatch.setattr(runtime, "_project", None)
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
