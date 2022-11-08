from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_profile_by_xuid(respx_mock, xbl_client):
    route = respx_mock.get("https://usersearch.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("usersearch_live_search"))
    )
    ret = await xbl_client.usersearch.get_live_search("tux")

    assert len(ret.results) == 8

    assert route.called
