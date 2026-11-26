import uuid

from ..definition.project import Project
from .. import runtime
from . import project_manager


def test_create_project(monkeypatch):
    test_uuid = uuid.uuid7()
    monkeypatch.setattr(uuid, "uuid7", lambda: test_uuid)
    project = project_manager.create_project("name")
    assert project == Project(test_uuid, "name")
    assert project.repo is None


def test_create_project_with_repo(monkeypatch):
    monkeypatch.setattr(uuid, "uuid7", lambda: uuid.UUID(int=1))
    repo = "https://github.com/example/repo.git"
    assert project_manager.create_project("name", repo=repo).repo == repo


def test_open_project_loads_project(monkeypatch):
    monkeypatch.setattr("app.runtime._project", None)
    project = Project(uuid.uuid7(), "open_name")
    assert project_manager.open_project(project) is project
    assert runtime.require_project() is project
