from uuid import uuid7

import pytest

from ..runtime import load_project
from ..definition.project import Project
from ..definition.task import Task
from ..definition.relation import RelationType
from . import relation_manager

TEST_TASKS = Task('a'), Task('b')
TEST_RELATION = RelationType.BLOCK, TEST_TASKS[0].id, TEST_TASKS[1].id


def test_add_relation():
    project = Project(uuid7(), 'test_add_relation', TEST_TASKS)
    load_project(project)
    result = relation_manager.add_relation(TEST_RELATION)
    assert result == [TEST_RELATION]
    assert TEST_RELATION in project.relations


def test_add_duplicate_relation():
    load_project(Project(uuid7(), 'test_add_duplicate_relation', TEST_TASKS, [TEST_RELATION]))
    with pytest.raises(ValueError):
        relation_manager.add_relation(TEST_RELATION)
