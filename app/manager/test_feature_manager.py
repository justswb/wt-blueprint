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


def test_update_feature_keeps_id():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    replacement = Feature('new', desc='new desc', tasks=[TEST_TASKS[1].id])
    result = feature_manager.update_feature(feature.id, replacement)
    assert result is replacement
    assert replacement.id == feature.id
    assert require_project().features == [replacement]


def test_update_feature_missing_raises_lookup_error():
    load_project(Project(uuid7(), 'p', TEST_TASKS))
    with pytest.raises(LookupError):
        feature_manager.update_feature(uuid7(), Feature('f'))


def test_update_feature_unknown_task_leaves_feature_unchanged():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    with pytest.raises(LookupError):
        feature_manager.update_feature(feature.id, Feature('new', tasks=[uuid7()]))
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]


def test_delete_feature_removes_it():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    assert feature_manager.delete_feature(feature.id) is feature
    assert require_project().features == []


def test_delete_feature_missing_raises_lookup_error():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    with pytest.raises(LookupError):
        feature_manager.delete_feature(uuid7())
    assert require_project().features == [feature]


def test_add_task_to_feature_appends():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    assert feature_manager.add_task_to_feature(feature.id, TEST_TASKS[1].id).tasks == [TEST_TASKS[0].id, TEST_TASKS[1].id]


def test_add_task_to_missing_feature_raises_lookup_error():
    load_project(Project(uuid7(), 'p', TEST_TASKS))
    with pytest.raises(LookupError):
        feature_manager.add_task_to_feature(uuid7(), TEST_TASKS[0].id)


def test_add_unknown_task_to_feature_raises_lookup_error():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    with pytest.raises(LookupError):
        feature_manager.add_task_to_feature(feature.id, uuid7())
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]


def test_add_existing_task_to_feature_raises_value_error():
    feature = Feature('f', tasks=[TEST_TASKS[0].id])
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], [feature]))
    with pytest.raises(ValueError):
        feature_manager.add_task_to_feature(feature.id, TEST_TASKS[0].id)
    assert require_project().features[0].tasks == [TEST_TASKS[0].id]


def test_add_same_task_to_two_features():
    features = [Feature('f1'), Feature('f2')]
    load_project(Project(uuid7(), 'p', TEST_TASKS, [], features))
    feature_manager.add_task_to_feature(features[0].id, TEST_TASKS[0].id)
    feature_manager.add_task_to_feature(features[1].id, TEST_TASKS[0].id)
    assert features[0].tasks == [TEST_TASKS[0].id]
    assert features[1].tasks == [TEST_TASKS[0].id]


def test_create_feature_unknown_task_raises_lookup_error():
    load_project(Project(uuid7(), 'p', TEST_TASKS))
    with pytest.raises(LookupError):
        feature_manager.create_feature(Feature('f', tasks=[uuid7()]))
    assert require_project().features == []
