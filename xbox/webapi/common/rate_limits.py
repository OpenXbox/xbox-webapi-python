from enum import Enum
from datetime import datetime, timedelta
from typing import Union
from pydantic import BaseModel


class TimePeriod(Enum):
    BURST = 15
    SUSTAIN = 300  # 5 minutes (300s)


class LimitType(Enum):
    WRITE = 0
    READ = 1


class IncrementResult(BaseModel):
    counter: int
    exceeded: bool


class RateLimit:
    def __init__(self, time_period: TimePeriod, limit: int):
        self.__time_period = time_period
        self.__limit = limit

        self.__exceeded: bool = False
        self.__counter = 0
        # No requests so far, so reset_after is None.
        self.__reset_after: Union[datetime, None] = None

    def get_time_period(self) -> "TimePeriod":
        return self.__time_period

    def get_reset_after(self) -> Union[datetime, None]:
        return self.__reset_after

    def is_exceeded(self) -> bool:
        self.__reset_counter_if_required()
        return self.__exceeded

    def increment(self) -> IncrementResult:
        self.__reset_counter_if_required()
        self.__counter += 1
        self.__check_if_exceeded()
        return IncrementResult(counter=self.__counter, exceeded=self.__exceeded)

    # Should be called after every inc of the counter
    def __check_if_exceeded(self):
        if not self.__exceeded:
            if self.__counter >= self.__limit:
                self.__exceeded = True
                self.__reset_after = datetime.now() + timedelta(
                    seconds=self.get_time_period().value
                )

    def __reset_counter_if_required(self):
        if self.__reset_after is not None and self.__exceeded:
            if self.__reset_after < datetime.now():
                self.__exceeded = False
                self.__counter = 0
                self.__reset_after = None
