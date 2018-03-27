"""
Enum helper class
"""
import enum


class StrEnum(str, enum.Enum):
    def __str__(self):
        return self.value


class IntEnum(int, enum.Enum):
    pass
