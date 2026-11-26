import uuid
from uuid import UUID

from ..runtime import load_project, require_project
from ..definition.project import Project


def create_project(name: str, repo: str | None = None) -> Project:
    return Project(uuid.uuid7(), name, repo=repo)


def open_project(project: Project) -> Project:
    load_project(project)
    return project


def get_project(proj_id: UUID) -> Project:
    project = require_project()
    if project.id != proj_id:
        raise LookupError(f'No loaded project with id {proj_id} was found')
    return project
