from dataclasses import dataclass, field
from uuid import UUID

from .task import Task
from .relation import Relation

@dataclass
class Project:
    id: UUID
    name: str
    tasks: list[Task] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    pass
