from datetime import datetime, timedelta
from httpx import Response
import pytest

from tests.common import get_response_json
from xbox.webapi.api.provider.ratelimitedprovider import RateLimitedProvider

from xbox.webapi.common.exceptions import RateLimitExceededException
from xbox.webapi.common.ratelimits import CombinedRateLimit
from xbox.webapi.common.ratelimits.models import TimePeriod


def helper_test_combinedratelimit(
    crl: CombinedRateLimit, burstLimit: int, sustainLimit: int
):
    burst = crl.get_limits_by_period(TimePeriod.BURST)
    sustain = crl.get_limits_by_period(TimePeriod.SUSTAIN)

    # These functions should return a list with one element
    assert type(burst) == list
    assert type(sustain) == list

    assert len(burst) == 1
    assert len(sustain) == 1

    # Check that their limits are what we expect
    assert burst[0].get_limit() == burstLimit
    assert sustain[0].get_limit() == sustainLimit


def test_ratelimitedprovider_rate_limits_same_rw_values(xbl_client):
    class child_class(RateLimitedProvider):
        RATE_LIMITS = {"burst": 1, "sustain": 2}

    instance = child_class(xbl_client)

    helper_test_combinedratelimit(instance.rate_limit_read, 1, 2)
    helper_test_combinedratelimit(instance.rate_limit_write, 1, 2)


def test_ratelimitedprovider_rate_limits_diff_rw_values(xbl_client):
    class child_class(RateLimitedProvider):
        RATE_LIMITS = {
            "burst": {"read": 1, "write": 2},
            "sustain": {"read": 3, "write": 4},
        }

    instance = child_class(xbl_client)

    helper_test_combinedratelimit(instance.rate_limit_read, 1, 3)
    helper_test_combinedratelimit(instance.rate_limit_write, 2, 4)


def test_ratelimitedprovider_rate_limits_mixed(xbl_client):
    class burst_diff(RateLimitedProvider):
        RATE_LIMITS = {"burst": {"read": 1, "write": 2}, "sustain": 3}

    burst_diff_inst = burst_diff(xbl_client)

    # Sustain values are the same (third paramater)
    helper_test_combinedratelimit(burst_diff_inst.rate_limit_read, 1, 3)
    helper_test_combinedratelimit(burst_diff_inst.rate_limit_write, 2, 3)

    class sustain_diff(RateLimitedProvider):
        RATE_LIMITS = {"burst": 4, "sustain": {"read": 5, "write": 6}}

    sustain_diff_inst = sustain_diff(xbl_client)

    # Burst values are the same (second paramater)
    helper_test_combinedratelimit(sustain_diff_inst.rate_limit_read, 4, 5)
    helper_test_combinedratelimit(sustain_diff_inst.rate_limit_write, 4, 6)


@pytest.mark.asyncio
async def test_ratelimits_exceeded_burst_only(respx_mock, xbl_client):
    async def make_request():
        route = respx_mock.get("https://peoplehub.xboxlive.com").mock(
            return_value=Response(200, json=get_response_json("people_friends_own"))
        )
        ret = await xbl_client.people.get_friends_own()

        assert len(ret.people) == 2
        assert route.called

    # Record the start time to ensure that the timeouts are the correct length
    start_time = datetime.now()

    # Make as many requests as possible without exceeding
    max_request_num = xbl_client.people.RATE_LIMITS["burst"]
    for i in range(max_request_num):
        await make_request()

    # Make another request, ensure that it raises the exception.
    with pytest.raises(RateLimitExceededException) as exception:
        await make_request()

    # Get the error instance from pytest
    ex: RateLimitExceededException = exception.value

    # Assert that the counter matches the max request num (should not have incremented above max value)
    assert ex.rate_limit.get_counter() == max_request_num

    # Get the timeout we were issued
    try_again_in = ex.rate_limit.get_reset_after()

    # Assert that the timeout is the correct length
    delta: timedelta = try_again_in - start_time
    assert delta.seconds == 15
