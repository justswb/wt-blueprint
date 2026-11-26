from http import HTTPStatus
import uuid

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import load_project
from ...definition.project import Project
from .common import require_project


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
    load_project(Project(uuid.uuid7(), "test_require_unloaded_project_name"))
    response = client.get(f'/{TEST_UUID}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    pass
