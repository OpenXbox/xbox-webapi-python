from datetime import datetime, timedelta
from httpx import Response
import pytest

from tests.common import get_response_json

from xbox.webapi.common.exceptions import RateLimitExceededException


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
