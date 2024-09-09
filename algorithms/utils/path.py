from dataclasses import dataclass


@dataclass
class Path:
    indexes: list[int]
    length: float
    name: str
