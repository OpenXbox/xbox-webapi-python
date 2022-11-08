from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_achievement_360_all(respx_mock, xbl_client):
    route = respx_mock.get("https://achievements.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("achievements_360_all"))
    )

    ret = await xbl_client.achievements.get_achievements_xbox360_all(
        "2669321029139235", 1297290392
    )

    assert ret.paging_info.total_records == 15
    assert route.called


@pytest.mark.asyncio
async def test_achievement_360_earned(respx_mock, xbl_client):
    route = respx_mock.get("https://achievements.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("achievements_360_earned"))
    )

    ret = await xbl_client.achievements.get_achievements_xbox360_earned(
        "2669321029139235", 1297290392
    )

    assert len(ret.achievements) == 1
    assert route.called


@pytest.mark.asyncio
async def test_achievement_360_recent_progress(respx_mock, xbl_client):
    route = respx_mock.get("https://achievements.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("achievements_360_recent_progress")
        )
    )

    ret = (
        await xbl_client.achievements.get_achievements_xbox360_recent_progress_and_info(
            xuid="2669321029139235"
        )
    )

    assert len(ret.titles) == 32
    assert route.called


@pytest.mark.asyncio
async def test_achievement_one_details(respx_mock, xbl_client):
    route = respx_mock.get("https://achievements.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("achievements_one_details"))
    )

    ret = await xbl_client.achievements.get_achievements_detail_item(
        xuid="2669321029139235",
        service_config_id="1370999b-fca2-4c53-8ec5-73493bcb67e5",
        achievement_id="39",
    )

    assert len(ret.achievements) == 1
    assert route.called


@pytest.mark.asyncio
async def test_achievement_one_gameprogress(respx_mock, xbl_client):
    route = respx_mock.get("https://achievements.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("achievements_one_gameprogress")
        )
    )

    ret = await xbl_client.achievements.get_achievements_xboxone_gameprogress(
        xuid="2669321029139235", title_id=219630713
    )

    assert len(ret.achievements) == 32
    assert route.called


@pytest.mark.asyncio
async def test_achievement_one_recent_progress(respx_mock, xbl_client):
    route = respx_mock.get("https://achievements.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("achievements_one_recent_progress")
        )
    )

    ret = (
        await xbl_client.achievements.get_achievements_xboxone_recent_progress_and_info(
            xuid="2669321029139235"
        )
    )

    assert len(ret.titles) == 32
    assert route.called
