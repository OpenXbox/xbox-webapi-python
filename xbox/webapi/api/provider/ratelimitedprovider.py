"""
RateLimitedProvider

Subclassed by providers with rate limit support
"""

from typing import Union
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.common.ratelimits.models import ParsedRateLimit


class RateLimitedProvider(BaseProvider):
    RATE_LIMITS: dict[str, Union[int, dict[str, int]]]

    def __init__(self, client):
        """
        Initialize Baseclass

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        # [commented out for testing] super().__init__(client)
        print(self.RATE_LIMITS)

        # Parse the rate limit dict
        burst_key = self.RATE_LIMITS["burst"]
        sustain_key = self.RATE_LIMITS["sustain"]

        burst_rate_limits = self.__parse_rate_limit_key(burst_key)
        sustain_rate_liits = self.__parse_rate_limit_key(sustain_key)

        print(burst_rate_limits)
        print(sustain_rate_liits)

    def __parse_rate_limit_key(
        self, key: Union[int, dict[str, int]]
    ) -> ParsedRateLimit:
        key_type = type(key)
        if key_type == int:
            return ParsedRateLimit(read=key, write=key)
        elif key_type == dict:
            # TODO: schema here?
            # Since the key-value pairs match we can just pass the dict to the model
            return ParsedRateLimit(**key)
            # return ParsedRateLimit(read=key["read"], write=key["write"])
