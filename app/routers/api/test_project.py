from http import HTTPStatus
import uuid

from fastapi.testclient import TestClient

from ...main import app
from ...runtime import require_project


BASE_URL = 'http://testserver/api/project/'
client = TestClient(app, BASE_URL)


def test_create_project(monkeypatch):
    test_uuid = uuid.uuid7()
    def mockreturn():
        return test_uuid
    monkeypatch.setattr(uuid, "uuid7", mockreturn)
    proj_name = "test_create_project"
    response = client.post(f'{BASE_URL}new', json={"name":proj_name})
    assert response.status_code == HTTPStatus.CREATED.value
    assert response.json() == {"id":str(test_uuid),"name":proj_name, "tasks":[]}
    pass
