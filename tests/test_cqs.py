from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_channel_list_download(respx_mock, xbl_client):
    route = respx_mock.get("https://cqs.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("cqs_get_channel_list"))
    )

    ret = await xbl_client.cqs.get_channel_list(
        locale_info="de-DE", headend_id="dbd2530a-fcd5-8ff0-b89d-20cd7e021502"
    )

    assert len(ret.channels) == 8
    assert route.called


@pytest.mark.asyncio
async def test_schedule_download(respx_mock, xbl_client):
    route = respx_mock.get("https://cqs.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("cqs_get_schedule"))
    )

    ret = await xbl_client.cqs.get_schedule(
        locale_info="de-DE",
        headend_id="dbd2530a-fcd5-8ff0-b89d-20cd7e021502",
        start_date="2018-03-20T23:50:00.000Z",
        duration_minutes=60,
        channel_skip=0,
        channel_count=5,
    )

    assert len(ret.channels) == 5
    assert route.called
