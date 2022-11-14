"""
RateLimitedProvider

Subclassed by providers with rate limit support
"""

from typing import Union
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.common.ratelimits.models import LimitType, ParsedRateLimit, TimePeriod
from xbox.webapi.common.ratelimits import CombinedRateLimit


class RateLimitedProvider(BaseProvider):
    RATE_LIMITS: dict[str, Union[int, dict[str, int]]]

    def __init__(self, client):
        """
        Initialize Baseclass

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        super().__init__(client)

        # Retrieve burst and sustain from the dict
        burst_key = self.RATE_LIMITS["burst"]
        sustain_key = self.RATE_LIMITS["sustain"]

        # Parse the rate limit dict values
        burst_rate_limits = self.__parse_rate_limit_key(burst_key, TimePeriod.BURST)
        sustain_rate_limits = self.__parse_rate_limit_key(
            sustain_key, TimePeriod.SUSTAIN
        )

        # Instanciate CombinedRateLimits for read and write respectively
        self.rate_limit_read = CombinedRateLimit(
            burst_rate_limits, sustain_rate_limits, type=LimitType.READ
        )
        self.rate_limit_write = CombinedRateLimit(
            burst_rate_limits, sustain_rate_limits, type=LimitType.WRITE
        )

    def __parse_rate_limit_key(
        self, key: Union[int, dict[str, int]], period: TimePeriod
    ) -> ParsedRateLimit:
        key_type = type(key)
        if key_type == int:
            return ParsedRateLimit(read=key, write=key, period=period)
        elif key_type == dict:
            # TODO: schema here?
            # Since the key-value pairs match we can just pass the dict to the model
            return ParsedRateLimit(**key, period=period)
            # return ParsedRateLimit(read=key["read"], write=key["write"])
