from enum import Enum
from pydantic import BaseModel


class TimePeriod(Enum):
    BURST = 15  # 15 seconds
    SUSTAIN = 300  # 5 minutes (300s)


class LimitType(Enum):
    WRITE = 0
    READ = 1


class IncrementResult(BaseModel):
    counter: int
    exceeded: bool


class ParsedRateLimit(BaseModel):
    read: int
    write: int
    period: TimePeriod
