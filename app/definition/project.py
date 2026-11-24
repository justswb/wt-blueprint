from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from .task import Task

@dataclass
class Project:
    id: UUID
    name: str
    tasks: List[Task] = field(default_factory=list)
    pass
