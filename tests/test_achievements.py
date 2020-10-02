import os

import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_achievement_360_all(aresponses, xbl_client):
    aresponses.add(
        "achievements.xboxlive.com", response=get_response("achievements_360_all")
    )

    ret = await xbl_client.achievements.get_achievements_xbox360_all(
        "2669321029139235", 1297290392
    )
    await xbl_client._auth_mgr.session.close()

    assert ret.paging_info.total_records == 15
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_achievement_360_earned(aresponses, xbl_client):
    aresponses.add(
        "achievements.xboxlive.com", response=get_response("achievements_360_earned")
    )

    ret = await xbl_client.achievements.get_achievements_xbox360_earned(
        "2669321029139235", 1297290392
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.achievements) == 1
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_achievement_360_recent_progress(aresponses, xbl_client):
    aresponses.add(
        "achievements.xboxlive.com",
        response=get_response("achievements_360_recent_progress"),
    )

    ret = (
        await xbl_client.achievements.get_achievements_xbox360_recent_progress_and_info(
            xuid="2669321029139235"
        )
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.titles) == 32
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_achievement_one_details(aresponses, xbl_client):
    aresponses.add(
        "achievements.xboxlive.com", response=get_response("achievements_one_details")
    )

    ret = await xbl_client.achievements.get_achievements_detail_item(
        xuid="2669321029139235",
        service_config_id="1370999b-fca2-4c53-8ec5-73493bcb67e5",
        achievement_id="39",
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.achievements) == 1
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_achievement_one_gameprogress(aresponses, xbl_client):
    aresponses.add(
        "achievements.xboxlive.com",
        response=get_response("achievements_one_gameprogress"),
    )

    ret = await xbl_client.achievements.get_achievements_xboxone_gameprogress(
        xuid="2669321029139235", title_id=219630713
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.achievements) == 32
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_achievement_one_recent_progress(aresponses, xbl_client):
    aresponses.add(
        "achievements.xboxlive.com",
        response=get_response("achievements_one_recent_progress"),
    )

    ret = (
        await xbl_client.achievements.get_achievements_xboxone_recent_progress_and_info(
            xuid="2669321029139235"
        )
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.titles) == 32
    aresponses.assert_plan_strictly_followed()
