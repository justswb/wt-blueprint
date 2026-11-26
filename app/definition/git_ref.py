from pydantic.dataclasses import dataclass

@dataclass
class GitRef:
    branch: str
    pr: int | None = None
    merge_commit: str | None = None
    pass
