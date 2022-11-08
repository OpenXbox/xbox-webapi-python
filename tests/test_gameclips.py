from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_gameclips_recent_xuid(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("gameclips_recent_xuid"))
    )
    ret = await xbl_client.gameclips.get_recent_clips_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_recent_xuid_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("gameclips_recent_xuid_titleid")
        )
    )
    ret = await xbl_client.gameclips.get_recent_clips_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_recent_own(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("gameclips_recent_own"))
    )
    ret = await xbl_client.gameclips.get_recent_own_clips(skip_items=0, max_items=25)

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_recent_own_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("gameclips_recent_own_titleid")
        )
    )
    ret = await xbl_client.gameclips.get_recent_own_clips(
        title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_recent_community(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("gameclips_recent_community"))
    )
    ret = await xbl_client.gameclips.get_recent_community_clips_by_title_id("219630713")

    assert len(ret.game_clips) == 99
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_saved_xuid(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("gameclips_saved_xuid"))
    )
    ret = await xbl_client.gameclips.get_saved_clips_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_saved_xuid_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("gameclips_saved_xuid_titleid")
        )
    )
    ret = await xbl_client.gameclips.get_saved_clips_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_saved_own(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("gameclips_saved_own"))
    )
    ret = await xbl_client.gameclips.get_saved_own_clips(skip_items=0, max_items=25)

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_saved_own_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("gameclips_saved_own_titleid")
        )
    )
    ret = await xbl_client.gameclips.get_saved_own_clips(
        title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.game_clips) == 25
    assert route.called


@pytest.mark.asyncio
async def test_gameclips_saved_community(respx_mock, xbl_client):
    route = respx_mock.get("https://gameclipsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("gameclips_saved_community"))
    )
    ret = await xbl_client.gameclips.get_saved_community_clips_by_title_id(219630713)

    assert len(ret.game_clips) == 99
    assert route.called
