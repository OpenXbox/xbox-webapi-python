import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_screenshots_recent_xuid(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_recent_xuid"),
    )
    ret = await xbl_client.screenshots.get_recent_screenshots_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_recent_xuid_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_recent_xuid_titleid"),
    )
    ret = await xbl_client.screenshots.get_recent_screenshots_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_recent_own(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_recent_own"),
    )
    ret = await xbl_client.screenshots.get_recent_own_screenshots(
        skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_recent_own_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_recent_own_titleid"),
    )
    ret = await xbl_client.screenshots.get_recent_own_screenshots(
        title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_recent_community(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_recent_community"),
    )
    ret = await xbl_client.screenshots.get_recent_community_screenshots_by_title_id(
        "219630713"
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 100

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_saved_xuid(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_saved_xuid"),
    )
    ret = await xbl_client.screenshots.get_saved_screenshots_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_saved_xuid_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_saved_xuid_titleid"),
    )
    ret = await xbl_client.screenshots.get_saved_screenshots_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_saved_own(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_saved_own"),
    )
    ret = await xbl_client.screenshots.get_saved_own_screenshots(
        skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_saved_own_titleid_filter(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_saved_own_titleid"),
    )
    ret = await xbl_client.screenshots.get_saved_own_screenshots(
        title_id=219630713, skip_items=0, max_items=25
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_screenshots_saved_community(aresponses, xbl_client):
    aresponses.add(
        "screenshotsmetadata.xboxlive.com",
        response=get_response("screenshots_saved_community"),
    )
    ret = await xbl_client.screenshots.get_saved_community_screenshots_by_title_id(
        219630713
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.screenshots) == 100

    aresponses.assert_plan_strictly_followed()
