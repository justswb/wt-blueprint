from http import HTTPStatus

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import require_project


BASE_URL = 'http://testserver/api/project/'
client = TestClient(app, BASE_URL)


def test_create_project():
    proj_name = "test_create_project"
    response = client.post(f'{BASE_URL}new', json={"name":proj_name})
    assert response.status_code == HTTPStatus.CREATED.value
    assert response.json() == {"id":str(require_project().id),"name":proj_name, "tasks":[]}
    pass
