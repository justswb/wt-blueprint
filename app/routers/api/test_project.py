from http import HTTPStatus
import uuid

from fastapi.testclient import TestClient

from ...main import app
from ... import runtime
from ...definition.project import Project


client = TestClient(app, 'http://testserver/api/project')


TEST_UUID = uuid.uuid7()
TEST_PROJ_JSON = {"id":str(TEST_UUID),"name":"test_proj_name", "tasks":[], "relations": [], "features": [], "repo": None}


def test_create_project(monkeypatch):
    monkeypatch.setattr(uuid, "uuid7", lambda: TEST_UUID)
    response = client.post('/new', json={"name":TEST_PROJ_JSON["name"]})
    assert response.status_code == HTTPStatus.CREATED.value
    assert response.json() == TEST_PROJ_JSON


def test_create_project_with_repo(monkeypatch):
    monkeypatch.setattr(uuid, "uuid7", lambda: TEST_UUID)
    repo = "https://github.com/example/repo.git"
    response = client.post('/new', json={"name":TEST_PROJ_JSON["name"], "repo":repo})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["repo"] == repo


def test_open_project(monkeypatch):
    monkeypatch.setattr(runtime, "_project", None)
    response = client.post('/', json=TEST_PROJ_JSON)
    assert response.status_code == HTTPStatus.OK
    assert runtime.require_project().id == TEST_UUID


def test_get_loaded_project(monkeypatch):
    monkeypatch.setattr(runtime, "_project", None)
    runtime.load_project(Project(TEST_UUID, "test_proj_name"))
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == str(TEST_UUID)


def test_get_unloaded_project_id_mismatch(monkeypatch):
    monkeypatch.setattr(runtime, "_project", None)
    runtime.load_project(Project(uuid.uuid7(), "test_require_unloaded_project_name"))
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_project_when_none_loaded(monkeypatch):
    monkeypatch.setattr(runtime, "_project", None)
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.BAD_REQUEST
