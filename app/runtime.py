from uuid import UUID

from .definition.project import Project

_project: Project | None = None

def load_project(target: Project) -> None:
    # if _project is not None: # confirm or autosave
    global _project
    _project = target
    pass

def require_project() -> Project:
    if _project is None:
        raise Exception('No project loaded')
    return _project
