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
    load_project(Project(uuid7(), 'test_add_relation', TEST_TASKS))
    result = relation_manager.add_relation(TEST_RELATION)
    assert result == [TEST_RELATION]
    assert TEST_RELATION in relation_manager.get_relations(TEST_TASKS[0].id)


def test_add_duplicate_relation():
    load_project(Project(uuid7(), 'test_add_duplicate_relation', TEST_TASKS, [TEST_RELATION]))
    with pytest.raises(ValueError):
        relation_manager.add_relation(TEST_RELATION)


def test_get_relations():
    load_project(Project(uuid7(), 'test_get_relations', TEST_TASKS, [TEST_RELATION]))
    assert relation_manager.get_relations(TEST_TASKS[0].id) == [TEST_RELATION]
    assert relation_manager.get_relations(TEST_TASKS[1].id) == [TEST_RELATION]
    assert relation_manager.get_relations(uuid7()) == []


def test_delete_relation():
    project = Project(uuid7(), 'test_delete_relation', TEST_TASKS, [TEST_RELATION])
    load_project(project)
    assert relation_manager.delete_relation(TEST_RELATION) == TEST_RELATION
    assert TEST_RELATION not in project.relations


def test_delete_missing_relation_raises_value_error():
    load_project(Project(uuid7(), 'test_delete_missing_relation', TEST_TASKS))
    with pytest.raises(ValueError):
        relation_manager.delete_relation(TEST_RELATION)
