from .definition.project import Project

project: Project | None = None

def assert_project_loaded() -> None:
    assert project is not None, 'No project loaded'
    pass
