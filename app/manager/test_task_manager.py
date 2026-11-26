from uuid import uuid7

from ..runtime import load_project, require_project
from ..definition.project import Project
from ..definition.task import Task
from ..definition.git_ref import GitRef
from . import task_manager


TEST_TASK = Task("test_task_name", uuid7(), "test_task_desc", Task.Status.DRAFT, GitRef('feat/a', 3, 'a' * 40))


def test_create_task_appends_and_returns_id():
    load_project(Project(uuid7(), "test_task_proj"))
    assert task_manager.create_task(TEST_TASK) == TEST_TASK.id
    assert require_project().tasks == [TEST_TASK]
