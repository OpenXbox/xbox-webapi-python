from enum import Enum
from pydantic import BaseModel


class IncrementResult(BaseModel):
    counter: int
    exceeded: bool


class TimePeriod(Enum):
    BURST = 15  # 15 seconds
    SUSTAIN = 300  # 5 minutes (300s)


class LimitType(Enum):
    WRITE = 0
    READ = 1
