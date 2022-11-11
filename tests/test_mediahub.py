from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_media_screenshots_own(respx_mock, xbl_client):
    route = respx_mock.post("https://mediahub.xboxlive.com/screenshots/search").mock(
        return_value=Response(200, json=get_response_json("mediahub_screenshots_own"))
    )
    ret = await xbl_client.mediahub.fetch_own_screenshots()

    assert len(ret.values) == 1
    assert route.called


@pytest.mark.asyncio
async def test_media_gameclips_own(respx_mock, xbl_client):
    route = respx_mock.post("https://mediahub.xboxlive.com/gameclips/search").mock(
        return_value=Response(200, json=get_response_json("mediahub_gameclips_own"))
    )
    ret = await xbl_client.mediahub.fetch_own_clips()

    assert len(ret.values) == 1
    assert route.called
