import asyncio
from datetime import datetime, timedelta

from httpx import Response
import pytest

from xbox.webapi.api.provider.ratelimitedprovider import RateLimitedProvider
from xbox.webapi.common.exceptions import RateLimitExceededException, XboxException
from xbox.webapi.common.ratelimits import CombinedRateLimit
from xbox.webapi.common.ratelimits.models import TimePeriod

from tests.common import get_response_json


def helper_test_combinedratelimit(
    crl: CombinedRateLimit, burstLimit: int, sustainLimit: int
):
    burst = crl.get_limits_by_period(TimePeriod.BURST)
    sustain = crl.get_limits_by_period(TimePeriod.SUSTAIN)

    # These functions should return a list with one element
    assert isinstance(burst, list)
    assert isinstance(sustain, list)

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


def test_ratelimitedprovider_rate_limits_missing_values_correct_type(xbl_client):
    class child_class(RateLimitedProvider):
        RATE_LIMITS = {"incorrect": "values"}

    with pytest.raises(XboxException) as exception:
        child_class(xbl_client)

    ex: XboxException = exception.value
    assert "RATE_LIMITS object missing required keys" in ex.args[0]


def test_ratelimitedprovider_rate_limits_not_set(xbl_client):
    class child_class(RateLimitedProvider):
        pass

    with pytest.raises(XboxException) as exception:
        child_class(xbl_client)

    ex: XboxException = exception.value
    assert "RateLimitedProvider as parent class but RATE_LIMITS not set!" in ex.args[0]


def test_ratelimitedprovider_rate_limits_incorrect_key_type(xbl_client):
    class child_class(RateLimitedProvider):
        RATE_LIMITS = {"burst": True, "sustain": False}

    with pytest.raises(XboxException) as exception:
        child_class(xbl_client)

    ex: XboxException = exception.value
    assert "RATE_LIMITS value types not recognised." in ex.args[0]


@pytest.mark.asyncio
async def test_ratelimits_exceeded_burst_only(respx_mock, xbl_client):
    async def make_request():
        route = respx_mock.get("https://social.xboxlive.com").mock(
            return_value=Response(200, json=get_response_json("people_summary_own"))
        )
        await xbl_client.people.get_friends_summary_own()

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
    assert delta.seconds == TimePeriod.BURST.value  # 15 seconds


async def helper_reach_and_wait_for_burst(
    make_request, start_time, burst_limit: int, expected_counter: int
):
    # Make as many requests as possible without exceeding the BURST limit.
    for _ in range(burst_limit):
        await make_request()

    # Make another request, ensure that it raises the exception.
    with pytest.raises(RateLimitExceededException) as exception:
        await make_request()

    # Get the error instance from pytest
    ex: RateLimitExceededException = exception.value

    # Assert that the counter matches the what we expect (burst, 2x burstm etc)
    assert ex.rate_limit.get_counter() == expected_counter

    # Get the reset_after value
    # (if we call it after waiting for it to expire the function will return None)
    burst_resets_after = ex.rate_limit.get_reset_after()

    # Wait for the burst limit timeout to elapse.
    await asyncio.sleep(TimePeriod.BURST.value)  # 15 seconds

    # Assert that the reset_after value has passed.
    assert burst_resets_after < datetime.now()


@pytest.mark.asyncio
async def test_ratelimits_exceeded_sustain_only(respx_mock, xbl_client):
    async def make_request():
        route = respx_mock.get("https://social.xboxlive.com").mock(
            return_value=Response(200, json=get_response_json("people_summary_own"))
        )
        await xbl_client.people.get_friends_summary_own()

        assert route.called

    # Record the start time to ensure that the timeouts are the correct length
    start_time = datetime.now()

    # Get the max requests for this route.
    max_request_num = xbl_client.people.RATE_LIMITS["sustain"]  # 30
    burst_max_request_num = xbl_client.people.RATE_LIMITS["burst"]  # 10

    # In this case, the BURST limit is three times that of SUSTAIN, so we need to exceed the burst limit three times.

    # Exceed the burst limit and wait for it to reset (10 requests)
    await helper_reach_and_wait_for_burst(
        make_request, start_time, burst_limit=burst_max_request_num, expected_counter=10
    )

    # Repeat: Exceed the burst limit and wait for it to reset (10 requests)
    # Counter (the sustain one will be returned)
    #         For (CombinedRateLimit).get_counter(), the highest counter is returned. (sustain in this case)
    await helper_reach_and_wait_for_burst(
        make_request, start_time, burst_limit=burst_max_request_num, expected_counter=20
    )

    # Now, make the rest of the requests (10 left, 20/30 done!)
    for _ in range(10):
        await make_request()

    # Wait for the burst limit to 'reset'.
    await asyncio.sleep(TimePeriod.BURST.value)  # 15 seconds

    # Now, we have made 30 requests.
    # The counters should be as follows:
    # - BURST: 0* (will reset on next check)
    # - SUSTAIN: 30
    # The next request we make should exceed the SUSTAIN rate limit.

    # Make another request, ensure that it raises the exception.
    with pytest.raises(RateLimitExceededException) as exception:
        await make_request()

    # Get the error instance from pytest
    ex: RateLimitExceededException = exception.value

    # Get the SingleRateLimit objects from the exception
    rl: CombinedRateLimit = ex.rate_limit
    burst = rl.get_limits_by_period(TimePeriod.BURST)[0]
    sustain = rl.get_limits_by_period(TimePeriod.SUSTAIN)[0]

    # Assert that we have only exceeded the sustain limit.
    assert not burst.is_exceeded()
    assert sustain.is_exceeded()

    # Assert that the counter matches the max request num (should not have incremented above max value)
    assert ex.rate_limit.get_counter() == max_request_num

    # Get the timeout we were issued
    try_again_in = ex.rate_limit.get_reset_after()

    # Assert that the timeout is the correct length
    # The SUSTAIN counter has not been reset during this test, so the try again in should be 300 seconds since we started this test.
    delta: timedelta = try_again_in - start_time
    assert delta.seconds == TimePeriod.SUSTAIN.value  # 300 seconds (5 minutes)
