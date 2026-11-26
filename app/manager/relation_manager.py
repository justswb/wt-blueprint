from ..definition.relation import Relation
from ..runtime import require_project


def add_relation(relation: Relation) -> list[Relation]:
    project = require_project()
    if relation in project.relations:
        raise ValueError('Given relation already exists')
    project.relations.append(relation)
    return [r for r in project.relations if relation[1] in r]
