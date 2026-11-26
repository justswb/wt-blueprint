from uuid import UUID

from ..definition.relation import Relation
from ..runtime import require_project


def add_relation(relation: Relation) -> list[Relation]:
    project = require_project()
    if relation in project.relations:
        raise ValueError('Given relation already exists')
    project.relations.append(relation)
    return get_relations(relation[1])


def get_relations(task_id: UUID) -> list[Relation]:
    return [r for r in require_project().relations if task_id in r]


def delete_relation(relation: Relation) -> Relation:
    project = require_project()
    idx = project.relations.index(relation)
    return project.relations.pop(idx)
