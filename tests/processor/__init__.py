from typing import NamedTuple


class MergeProperties(NamedTuple):
    timestamp: int
    atom: str
    atom_base: str
    atom_version: str
    count_n: str
    count_m: str
