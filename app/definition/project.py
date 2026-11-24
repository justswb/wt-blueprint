from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID

from .task import Task

@dataclass
class Project:
    id: UUID
    name: str
    tasks: Dict[UUID, Task] = field(default_factory=dict)
    pass
