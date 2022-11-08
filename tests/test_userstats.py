from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_userstats_by_scid(respx_mock, xbl_client):
    route = respx_mock.get("https://userstats.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("userstats_by_scid"))
    )
    ret = await xbl_client.userstats.get_stats(
        "2669321029139235", "1370999b-fca2-4c53-8ec5-73493bcb67e5"
    )

    assert len(ret.statlistscollection) == 1

    assert route.called


@pytest.mark.asyncio
async def test_userstats_by_scid_with_metadata(respx_mock, xbl_client):
    route = respx_mock.get("https://userstats.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("userstats_by_scid_with_metadata")
        )
    )
    ret = await xbl_client.userstats.get_stats_with_metadata(
        "2669321029139235", "1370999b-fca2-4c53-8ec5-73493bcb67e5"
    )

    assert len(ret.statlistscollection) == 1

    assert route.called


@pytest.mark.asyncio
async def test_userstats_batch(respx_mock, xbl_client):
    route = respx_mock.post("https://userstats.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("userstats_batch"))
    )
    ret = await xbl_client.userstats.get_stats_batch(["2584878536129841"], "1717113201")

    assert len(ret.statlistscollection) == 1
    assert len(ret.groups) == 1
    assert len(ret.groups[0].statlistscollection) > 0

    assert route.called


@pytest.mark.asyncio
async def test_userstats_batch_by_scid(respx_mock, xbl_client):
    route = respx_mock.post("https://userstats.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("userstats_batch_by_scid"))
    )
    ret = await xbl_client.userstats.get_stats_batch_by_scid(
        ["2669321029139235"], "1370999b-fca2-4c53-8ec5-73493bcb67e5"
    )

    assert len(ret.statlistscollection) == 1
    assert len(ret.groups) == 1
    assert len(ret.groups[0].statlistscollection) == 0

    assert route.called
