from dataclasses import dataclass, field
from uuid import UUID

from .task import Task

@dataclass
class Project:
    id: UUID
    name: str
    tasks: dict[UUID, Task] = field(default_factory=dict)
    pass
