from typing import Annotated

from pydantic import PositiveInt, StringConstraints
from pydantic.dataclasses import dataclass

@dataclass
class GitRef:
    branch: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    pr: PositiveInt | None = None
    merge_commit: Annotated[str, StringConstraints(to_lower=True, pattern=r'^[0-9a-fA-F]{40}$')] | None = None
    pass
