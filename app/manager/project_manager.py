import uuid

from ..definition.project import Project


def create_project(name: str, repo: str | None = None) -> Project:
    return Project(uuid.uuid7(), name, repo=repo)
