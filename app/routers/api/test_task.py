from http import HTTPStatus
from uuid import UUID, uuid7

from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from ...main import app
from ...runtime import load_project
from ...definition.project import Project
from ...definition.task import Task
from ...definition.feature import Feature
from ...definition.git_ref import GitRef
from ...definition.relation import RelationType
from .common import find_task, get_relations, require_project

client = TestClient(app, 'http://testserver/api/task')


TEST_TASK = Task("test_task_name", uuid7(), "test_task_desc", Task.Status.DRAFT)
def task_to_dict(t: Task) -> dict:
    return TypeAdapter(Task).dump_python(t, mode='json')


def test_create_task():
    load_project(Project(uuid7(), "test_task_proj"))
    request_json = {k: v for k, v in task_to_dict(TEST_TASK).items() if k != 'id'}
    response = client.post('/', json=request_json)
    assert response.status_code == HTTPStatus.CREATED
    assert find_task(TEST_TASK.id) is not None
    pass


def test_get_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    response = client.get(f'/{TEST_TASK.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [0, task_to_dict(TEST_TASK)]
    pass


def test_update_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    request_json = {k: v for k, v in task_to_dict(TEST_TASK).items() if k != 'id'}
    request_json['name'] = 'mutation_task_name'
    response = client.post(f'/{TEST_TASK.id}', json=request_json)
    assert response.status_code == HTTPStatus.ACCEPTED
    assert find_task(TEST_TASK.id)[1].name == request_json['name']
    pass


def test_delete_task():
    load_project(Project(uuid7(), "test_task_proj", [TEST_TASK]))
    response = client.delete(f'/{TEST_TASK.id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert find_task(TEST_TASK.id) == (-1, None)
    pass


def test_delete_task_removes_feature_refs():
    tasks = Task('a'), Task('b')
    features = [Feature('f1', uuid7(), '', [tasks[0].id, tasks[1].id]), Feature('f2', uuid7(), '', [tasks[0].id])]
    load_project(Project(uuid7(), 'test_task_proj', list(tasks), [], features))
    response = client.delete(f'/{tasks[0].id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    proj_features = require_project().features
    assert all(tasks[0].id not in f.tasks for f in proj_features)
    assert tasks[1].id in proj_features[0].tasks
    pass


def test_delete_task_removes_relations():
    a = Task('a')
    b = Task('b')
    c = Task('c')
    relation_bc = (RelationType.BLOCK, b.id, c.id)
    load_project(Project(uuid7(), "test_task_proj", [a, b, c], [
        (RelationType.BLOCK, a.id, b.id),
        (RelationType.BLOCK, c.id, a.id),
        relation_bc,
    ]))
    response = client.delete(f'/{a.id}')
    assert response.status_code == HTTPStatus.ACCEPTED
    assert get_relations(a.id) == []
    assert relation_bc in get_relations(b.id)
    pass


def test_task_git_ref():
    load_project(Project(uuid7(), "test_task_proj"))
    ref = GitRef('feat/a', 3, 'a' * 40)
    response = client.post('/', json={'name': 'a', 'ref': {'branch': ref.branch, 'pr': ref.pr, 'merge_commit': ref.merge_commit}})
    assert response.status_code == HTTPStatus.CREATED
    _, task = find_task(UUID(response.json()))
    assert task.ref == ref
    response = client.get(f'/{task.id}')
    assert response.json()[1]['ref'] == {'branch': 'feat/a', 'pr': 3, 'merge_commit': 'a' * 40}
    pass


def test_task_without_git_ref():
    load_project(Project(uuid7(), "test_task_proj"))
    response = client.post('/', json={'name': 'a'})
    assert response.status_code == HTTPStatus.CREATED
    assert find_task(UUID(response.json()))[1].ref is None
    pass
