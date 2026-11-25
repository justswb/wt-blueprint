from dataclasses import field
from enum import Enum
from uuid import UUID, uuid7

from pydantic.json_schema import SkipJsonSchema
from pydantic.dataclasses import dataclass

@dataclass
class Task:
    class Status(Enum):
        DRAFT = 'draft'
        READY = 'ready'
        IN_PROGRESS = 'in progress'
        HOLD = 'hold'
        DONE = 'done'
        pass

    class Relation(Enum):
        BLOCKING = 'blocking'
        BLOCKED_BY = 'blocked by'
        pass

    name: str
    id: SkipJsonSchema[UUID] = field(default_factory=uuid7)
    desc: str = ''
    status: Status = Status.DRAFT
    relations: dict[Relation, list[UUID]] = field(default_factory=dict)
    pass
