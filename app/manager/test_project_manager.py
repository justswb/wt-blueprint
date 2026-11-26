import uuid

import pytest

from ..runtime import load_project
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


def test_open_project_loads_it(monkeypatch):
    monkeypatch.setattr("app.runtime._project", None)
    project = Project(uuid.uuid7(), "open_name")
    assert project_manager.open_project(project) is project
    assert project_manager.get_project(project.id) is project


def test_get_project_mismatched_id_raises_lookup_error(monkeypatch):
    monkeypatch.setattr("app.runtime._project", None)
    load_project(Project(uuid.uuid7(), "loaded"))
    with pytest.raises(LookupError):
        project_manager.get_project(uuid.uuid7())


def test_get_project_not_loaded_raises(monkeypatch):
    monkeypatch.setattr("app.runtime._project", None)
    with pytest.raises(Exception, match="No project loaded"):
        project_manager.get_project(uuid.uuid7())
