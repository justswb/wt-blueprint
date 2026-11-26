import pytest
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


def test_find_task_returns_index_and_task():
    b = Task('b')
    load_project(Project(uuid7(), 'p', [Task('a'), b]))
    assert task_manager.find_task(b.id) == (1, b)


def test_find_task_missing_raises_lookup_error():
    load_project(Project(uuid7(), 'p', [Task('a')]))
    missing = uuid7()
    with pytest.raises(LookupError, match=str(missing)):
        task_manager.find_task(missing)


def test_get_task_returns_index_and_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    assert task_manager.get_task(TEST_TASK.id) == (0, TEST_TASK)


def test_get_task_missing_raises_lookup_error():
    load_project(Project(uuid7(), 'p'))
    with pytest.raises(LookupError):
        task_manager.get_task(uuid7())


def test_update_task_replaces_and_keeps_id():
    original = Task('old')
    load_project(Project(uuid7(), 'p', [original]))
    replacement = Task('new')
    result = task_manager.update_task(original.id, replacement)
    assert result is replacement
    assert replacement.id == original.id
    assert require_project().tasks == [replacement]


def test_update_task_missing_raises_lookup_error():
    load_project(Project(uuid7(), 'p'))
    with pytest.raises(LookupError):
        task_manager.update_task(uuid7(), Task('x'))


def test_update_done_task_to_done_raises_permission_error():
    done = Task('done', status=Task.Status.DONE)
    load_project(Project(uuid7(), 'p', [done]))
    with pytest.raises(PermissionError):
        task_manager.update_task(done.id, Task('changed', status=Task.Status.DONE))
    assert require_project().tasks == [done]


def test_update_done_task_to_other_status_clears_pr_and_merge_commit():
    done = Task('done', status=Task.Status.DONE, ref=GitRef('feat/a', 3, 'a' * 40))
    load_project(Project(uuid7(), 'p', [done]))
    replacement = Task('reopened', status=Task.Status.IN_PROGRESS, ref=GitRef('feat/a', 3, 'a' * 40))
    result = task_manager.update_task(done.id, replacement)
    assert result.status == Task.Status.IN_PROGRESS
    assert result.ref == GitRef('feat/a', None, None)
    assert require_project().tasks == [result]
