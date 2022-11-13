from datetime import datetime, timedelta
from typing import Union

from xbox.webapi.common.ratelimits.models import TimePeriod, LimitType, IncrementResult


class SingleRateLimit:
    def __init__(self, time_period: TimePeriod, type: LimitType, limit: int):
        self.__time_period = time_period
        self.__type = type
        self.__limit = limit

        self.__exceeded: bool = False
        self.__counter = 0
        # No requests so far, so reset_after is None.
        self.__reset_after: Union[datetime, None] = None

    def get_time_period(self) -> "TimePeriod":
        return self.__time_period

    def get_limit_type(self) -> "LimitType":
        return self.__type

    def get_reset_after(self) -> Union[datetime, None]:
        return self.__reset_after

    def is_exceeded(self) -> bool:
        self.__reset_counter_if_required()
        return self.__exceeded

    def increment(self) -> IncrementResult:
        # Call a function to check if the counter should be reset
        self.__reset_counter_if_required()

        # Increment the counter
        self.__counter += 1

        # If the counter is 1, (first request after a reset) set the reset_after value.
        if self.__counter == 1:
            self.__set_reset_after()

        # Check to see if we have now exceeded the request limit
        self.__check_if_exceeded()

        # Return an instance of IncrementResult
        return IncrementResult(counter=self.__counter, exceeded=self.__exceeded)

    # Should be called after every inc of the counter
    def __check_if_exceeded(self):
        if not self.__exceeded:
            if self.__counter >= self.__limit:
                self.__exceeded = True
                # reset-after is now dependent on the time since the first request of this cycle.
                # self.__set_reset_after()

    def __reset_counter_if_required(self):
        # Check to make sure reset_after is not None
        # - This is the case if this function is called before the counter
        #   is incremented after a reset / new instantiation
        if self.__reset_after is not None:
            if self.__reset_after < datetime.now():
                self.__exceeded = False
                self.__counter = 0
                self.__reset_after = None

    def __set_reset_after(self):
        self.__reset_after = datetime.now() + timedelta(
            seconds=self.get_time_period().value
        )
