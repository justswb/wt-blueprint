import uuid

from ..definition.project import Project
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
