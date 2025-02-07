from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import List, Union

from xbox.webapi.common.ratelimits.models import (
    IncrementResult,
    LimitType,
    ParsedRateLimit,
    TimePeriod,
)


class RateLimit(metaclass=ABCMeta):
    """
    Abstract class for varying implementations/types of rate limits.
    All methods in this class are overriden in every implementation.
    However, different implementations may have additional functions not present in this parent abstract class.

    A class implementing RateLimit functions without any external threads.
    When the first increment request is recieved (after a counter reset or a new instaniciation)
    a reset_after variable is set detailing when the rate limit(s) reset.

    Upon each function invokation, the reset_after variable is checked and the timer is automatically reset if the reset_after time has passed.
    """

    @abstractmethod
    def get_counter(self) -> int:
        # Docstrings are defined in child classes due to their differing implementations.
        pass

    @abstractmethod
    def get_reset_after(self) -> Union[datetime, None]:
        # Docstrings are defined in child classes due to their differing implementations.
        pass

    @abstractmethod
    def is_exceeded(self) -> bool:
        # Docstrings are defined in child classes due to their differing implementations.
        pass

    @abstractmethod
    def increment(self) -> IncrementResult:
        """
        The increment function adds one to the rate limit request counter.

        If the reset_after time has passed, the counter will first be reset before counting the request.

        When the counter hits 1, the reset_after time is calculated and stored.

        This function returns an `IncrementResult` object, containing the keys `counter: int` and `exceeded: bool`.
        This can be used by the caller to determine the current state of the rate-limit object without making an additional function call.
        """

        pass


class SingleRateLimit(RateLimit):
    """
    A rate limit implementation for a single rate limit, such as a burst or sustain limit.
    This class is mainly used by the CombinedRateLimit class.
    """

    def __init__(self, time_period: TimePeriod, type: LimitType, limit: int):
        self.__time_period = time_period
        self.__type = type
        self.__limit = limit

        self.__exceeded: bool = False
        self.__counter = 0
        # No requests so far, so reset_after is None.
        self.__reset_after: Union[datetime, None] = None

    def get_counter(self) -> int:
        """
        This function returns the current request counter variable.
        """

        return self.__counter

    def get_time_period(self) -> "TimePeriod":
        return self.__time_period

    def get_limit(self) -> int:
        return self.__limit

    def get_limit_type(self) -> "LimitType":
        return self.__type

    def get_reset_after(self) -> Union[datetime, None]:
        """
        This getter returns the current state of the reset_after counter.

        If the counter in use, it's corresponding `datetime` object is returned.

        If the counter is not in use, `None` is returned.
        """

        return self.__reset_after

    def is_exceeded(self) -> bool:
        """
        This functions returns `True` if the rate limit has been exceeded.
        """

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
    """
    A rate limit implementation for multiple rate limits, such as burst and sustain.

    """

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

    def get_counter(self) -> int:
        """
        This function returns the request counter with the **highest** value.

        A `CombinedRateLimit` consists of multiple different rate limits, which may have differing counter values.
        """

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
        """
        This getter returns either a `datetime` object or `None` object depending on the status of the rate limit.

        If the counter is in use, the rate limit with the **latest** reset_after is returned.

        This is so that this function can reliably be used as a indicator of when all rate limits have been reset.

        If the counter is not in use, `None` is returned.
        """

        # Get a list of limits that *have been exceeded*
        dates_exceeded_only = filter(lambda limit: limit.is_exceeded(), self.__limits)

        # Map self.__limits to (limit).get_reset_after()
        dates_map = map(lambda limit: limit.get_reset_after(), dates_exceeded_only)

        # Convert the map object to a list
        dates = list(dates_map)

        # Construct a new list with only elements of instance datetime
        # (Effectively filtering out any None elements)
        dates_valid = [elem for elem in dates if isinstance(elem, datetime)]

        # If dates_valid has any elements, return the one with the *later* timestamp.
        # This means that if two or more limits have been exceeded, we wait for both to have reset (by returning the later timestamp)
        if len(dates_valid) != 0:
            # By default dates are sorted with the earliest date first.
            # We will set reverse=True so that the first element is the later date.
            dates_valid.sort(reverse=True)

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
        """
        This function returns `True` if **any** rate limit has been exceeded.

        It behaves like an OR logic gate.
        """

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

        # SPEC: Let's pick the *higher* counter
        # By default, sorted() returns in ascending order, so let's set reverse=True
        # This means that the result with the highest counter will be the first element.
        results_sorted = sorted(results, key=lambda i: i.counter, reverse=True)

        # Create an instance of IncrementResult and return it.
        return IncrementResult(
            counter=results_sorted[
                0
            ].counter,  # Use the highest counter (sorted in descending order)
            exceeded=self.is_exceeded(),  # Call self.is_exceeded (True if any limit has been exceeded, like an OR gate.)
        )
