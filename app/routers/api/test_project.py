from http import HTTPStatus

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import require_project


client = TestClient(app)


def test_create_project():
    proj_name = "test_create_project"
    response = client.post('/new', json={"name":proj_name})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id":str(require_project().id),"name":proj_name, "tasks":[]}
    pass
