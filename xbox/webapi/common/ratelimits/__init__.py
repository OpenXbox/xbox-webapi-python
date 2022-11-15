from datetime import datetime, timedelta
from typing import Union, List

from xbox.webapi.common.ratelimits.models import (
    ParsedRateLimit,
    TimePeriod,
    LimitType,
    IncrementResult,
)

from abc import ABCMeta, abstractmethod


class RateLimit(metaclass=ABCMeta):
    @abstractmethod
    def get_counter(self) -> int:
        pass

    @abstractmethod
    def get_reset_after(self) -> Union[datetime, None]:
        pass

    @abstractmethod
    def is_exceeded(self) -> bool:
        pass

    @abstractmethod
    def increment(self) -> IncrementResult:
        pass


class SingleRateLimit(RateLimit):
    def __init__(self, time_period: TimePeriod, type: LimitType, limit: int):
        self.__time_period = time_period
        self.__type = type
        self.__limit = limit

        self.__exceeded: bool = False
        self.__counter = 0
        # No requests so far, so reset_after is None.
        self.__reset_after: Union[datetime, None] = None

    def get_counter(self) -> int:
        return self.__counter

    def get_time_period(self) -> "TimePeriod":
        return self.__time_period

    def get_limit(self) -> int:
        return self.__limit

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


class CombinedRateLimit(RateLimit):
    def __init__(self, *parsed_limits: ParsedRateLimit, type: LimitType):
        # *parsed_limits is a tuple

        # Create a SingleRateLimit instance for each limit
        self.__limits: list[SingleRateLimit] = []

        for limit in parsed_limits:
            # Use the type param (enum LimitType) to determine which limit to select
            limit_num = limit.read if type == LimitType.READ else limit.write

            # Create a new instance of SingleRateLimit and append it to the limits array.
            srl = SingleRateLimit(limit.period, type, limit_num)
            self.__limits.append(srl)

        # DEBUG: print them
        for i in self.__limits:
            print(
                "Added limit of type %s, limit %s, and limit %i"
                % (i.get_limit_type(), i.get_time_period(), i._SingleRateLimit__limit)
            )

    def get_counter(self) -> int:
        # Map self.__limits to (limit).get_counter()
        counter_map = map(lambda limit: limit.get_counter(), self.__limits)
        counters = list(counter_map)

        # Sort the counters list by value
        # reverse=True to get highest first
        counters.sort(reverse=True)

        # Return the highest value
        return counters[0]

    # We don't want a datetime response for a limit that has not been exceeded.
    # Otherwise eg. 10 burst requests -> 300s timeout (should be 30 (burst exceeded), 300s (not exceeded)
    def get_reset_after(self) -> Union[datetime, None]:
        # Get a list of limits that *have been exceeded*
        dates_exceeded_only = filter(lambda limit: limit.is_exceeded(), self.__limits)

        # Map self.__limits to (limit).get_reset_after()
        dates_map = map(lambda limit: limit.get_reset_after(), dates_exceeded_only)

        # Convert the map object to a list
        dates = list(dates_map)

        # Construct a new list with only elements of instance datetime
        # (Effectively filtering out any None elements)
        dates_valid = [elem for elem in dates if type(elem) == datetime]

        # If dates_valid has any elements, return the one with the *later* timestamp.
        # This means that if two or more limits have been exceeded, we wait for both to have reset (by returning the later timestamp)
        if len(dates_valid) != 0:
            dates_valid[0].isoformat
            print(
                "Valid dates BEFORE sorting: %s"
                % list(map(lambda i: i.isoformat(), dates_valid))
            )
            # By default dates are sorted with the earliest date first.
            # We will set reverse=True so that the first element is the later date.
            dates_valid.sort(reverse=True)

            print(
                "Valid dates AFTER sorting:  %s"
                % list(map(lambda i: i.isoformat(), dates_valid))
            )

            # Return the datetime object.
            return dates_valid[0]

        # dates_valid has no elements, return None
        return None

    # list -> List (typing.List) https://stackoverflow.com/a/63460173
    def get_limits(self) -> List[SingleRateLimit]:
        return self.__limits

    # list -> List (typing.List) https://stackoverflow.com/a/63460173
    def get_limits_by_period(self, period: TimePeriod) -> List[SingleRateLimit]:
        # Filter the list for the given LimitType
        matches = filter(lambda limit: limit.get_time_period() == period, self.__limits)
        # Convert the filter object to a list and return it
        return list(matches)

    def is_exceeded(self) -> bool:
        # Map self.__limits to (limit).is_exceeded()
        is_exceeded_map = map(lambda limit: limit.is_exceeded(), self.__limits)
        is_exceeded_list = list(is_exceeded_map)

        # Return True if any variable in list is True
        return True in is_exceeded_list

    def increment(self) -> IncrementResult:
        # Increment each limit
        results: list[IncrementResult] = []
        for limit in self.__limits:
            result = limit.increment()
            results.append(result)

        # SPEC: Which counter should be picked here?
        # For now, let's pick the *higher* counter
        # (should incrementResult even include the counter?)
        results[1].counter = 5

        # By default, sorted() returns in ascending order, so let's set reverse=True
        # This means that the result with the highest counter will be the first element.
        results_sorted = sorted(results, key=lambda i: i.counter, reverse=True)

        # Create an instance of IncrementResult and return it.
        return IncrementResult(
            counter=results_sorted[
                0
            ].counter,  # Use the highest counter (sorted in descending order)
            exceeded=self.is_exceeded(),  # Call self.is_exceeded (True if any limit has been exceeded, a-la an OR gate.)
        )
