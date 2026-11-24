from dataclasses import dataclass, field
from uuid import UUID

from .task import Task

@dataclass
class Project:
    id: UUID
    name: str
    tasks: list[Task] = field(default_factory=list)
    pass
