import pytest
from uuid import uuid7

from ..runtime import load_project, require_project
from ..definition.project import Project
from ..definition.task import Task
from ..definition.feature import Feature
from ..definition.git_ref import GitRef
from . import feature_manager


TEST_TASKS = Task('a'), Task('b')


def test_create_feature_appends_and_returns_id():
    load_project(Project(uuid7(), 'p', TEST_TASKS))
    feature = Feature('f', tasks=[TEST_TASKS[0].id], ref=GitRef('feat/f', 7, 'b' * 40))
    assert feature_manager.create_feature(feature) == feature.id
    assert require_project().features == [feature]


def test_get_feature_returns_feature():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    assert feature_manager.get_feature(feature.id) is feature


def test_find_feature_missing_raises_lookup_error():
    load_project(Project(uuid7(), 'p', TEST_TASKS))
    with pytest.raises(LookupError):
        feature_manager.find_feature(uuid7())


def test_get_features_by_task_returns_matching_features():
    features = [
        Feature('f1', tasks=[TEST_TASKS[0].id, TEST_TASKS[1].id]),
        Feature('f2', tasks=[TEST_TASKS[0].id]),
        Feature('f3', tasks=[TEST_TASKS[1].id]),
    ]
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], features))
    assert feature_manager.get_features_by_task(TEST_TASKS[0].id) == [features[0], features[1]]
    assert feature_manager.get_features_by_task(uuid7()) == []


def test_create_feature_unknown_task_raises_lookup_error():
    load_project(Project(uuid7(), 'p', TEST_TASKS))
    with pytest.raises(LookupError):
        feature_manager.create_feature(Feature('f', tasks=[uuid7()]))
    assert require_project().features == []
