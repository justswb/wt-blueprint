from enum import Enum
from uuid import UUID


class RelationType(Enum):
    BLOCK = 'block'
    pass

type Relation = tuple[RelationType, UUID, UUID]
