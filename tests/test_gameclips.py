import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_gameclips_recent_xuid(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com", response=get_response("gameclips_recent_xuid")
    )
    ret = await xbl_client.gameclips.get_recent_clips_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_recent_xuid_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com",
        response=get_response("gameclips_recent_xuid_titleid"),
    )
    ret = await xbl_client.gameclips.get_recent_clips_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_recent_own(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com", response=get_response("gameclips_recent_own")
    )
    ret = await xbl_client.gameclips.get_recent_own_clips(skip_items=0, max_items=25)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_recent_own_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com",
        response=get_response("gameclips_recent_own_titleid"),
    )
    ret = await xbl_client.gameclips.get_recent_own_clips(
        title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_recent_community(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com",
        response=get_response("gameclips_recent_community"),
    )
    ret = await xbl_client.gameclips.get_recent_community_clips_by_title_id("219630713")
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 99
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_saved_xuid(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com", response=get_response("gameclips_saved_xuid")
    )
    ret = await xbl_client.gameclips.get_saved_clips_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_saved_xuid_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com",
        response=get_response("gameclips_saved_xuid_titleid"),
    )
    ret = await xbl_client.gameclips.get_saved_clips_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_saved_own(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com", response=get_response("gameclips_saved_own")
    )
    ret = await xbl_client.gameclips.get_saved_own_clips(skip_items=0, max_items=25)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_saved_own_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com",
        response=get_response("gameclips_saved_own_titleid"),
    )
    ret = await xbl_client.gameclips.get_saved_own_clips(
        title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 25
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_gameclips_saved_community(aresponses, xbl_client):
    aresponses.add(
        "gameclipsmetadata.xboxlive.com",
        response=get_response("gameclips_saved_community"),
    )
    ret = await xbl_client.gameclips.get_saved_community_clips_by_title_id(219630713)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.game_clips) == 99
    aresponses.assert_plan_strictly_followed()
