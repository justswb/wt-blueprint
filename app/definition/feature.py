from dataclasses import field
from uuid import UUID, uuid7

from pydantic.json_schema import SkipJsonSchema
from pydantic.dataclasses import dataclass

from .git_ref import GitRef

@dataclass
class Feature:
    name: str
    id: SkipJsonSchema[UUID] = field(default_factory=uuid7)
    desc: str = ''
    tasks: list[UUID] = field(default_factory=list)
    ref: GitRef | None = None
    pass
