from dataclasses import dataclass
from enum import Enum


class ReadDirection(Enum):
    LTR = "ltr"
    RTL = "rtl"


class LineOffset(Enum):
    BASELINE = 0
    TOPLINE = 1
    CENTERED = 2


@dataclass(init=True, frozen=True)
class PostDocument():
    name: str
    project: str
    main_script: str
    read_script: ReadDirection = ReadDirection.LTR
    line_offset: LineOffset = LineOffset.BASELINE
    tags: list[str] = []
