import uuid

from ..runtime import load_project
from ..definition.project import Project


def create_project(name: str, repo: str | None = None) -> Project:
    return Project(uuid.uuid7(), name, repo=repo)


def open_project(project: Project) -> Project:
    load_project(project)
    return project
