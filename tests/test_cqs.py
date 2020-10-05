import os

import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_channel_list_download(aresponses, xbl_client):
    aresponses.add("cqs.xboxlive.com", response=get_response("cqs_get_channel_list"))

    ret = await xbl_client.cqs.get_channel_list(
        locale_info="de-DE", headend_id="dbd2530a-fcd5-8ff0-b89d-20cd7e021502"
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.channels) == 8
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_schedule_download(aresponses, xbl_client):
    aresponses.add("cqs.xboxlive.com", response=get_response("cqs_get_schedule"))

    ret = await xbl_client.cqs.get_schedule(
        locale_info="de-DE",
        headend_id="dbd2530a-fcd5-8ff0-b89d-20cd7e021502",
        start_date="2018-03-20T23:50:00.000Z",
        duration_minutes=60,
        channel_skip=0,
        channel_count=5,
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.channels) == 5
    aresponses.assert_plan_strictly_followed()
