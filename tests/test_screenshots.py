from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_screenshots_recent_xuid(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("screenshots_recent_xuid"))
    )
    ret = await xbl_client.screenshots.get_recent_screenshots_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_recent_xuid_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("screenshots_recent_xuid_titleid")
        )
    )
    ret = await xbl_client.screenshots.get_recent_screenshots_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_recent_own(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("screenshots_recent_own"))
    )
    ret = await xbl_client.screenshots.get_recent_own_screenshots(
        skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_recent_own_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("screenshots_recent_own_titleid")
        )
    )
    ret = await xbl_client.screenshots.get_recent_own_screenshots(
        title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_recent_community(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("screenshots_recent_community")
        )
    )
    ret = await xbl_client.screenshots.get_recent_community_screenshots_by_title_id(
        "219630713"
    )

    assert len(ret.screenshots) == 100

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_saved_xuid(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("screenshots_saved_xuid"))
    )
    ret = await xbl_client.screenshots.get_saved_screenshots_by_xuid(
        "2669321029139235", skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_saved_xuid_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("screenshots_saved_xuid_titleid")
        )
    )
    ret = await xbl_client.screenshots.get_saved_screenshots_by_xuid(
        "2669321029139235", title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_saved_own(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("screenshots_saved_own"))
    )
    ret = await xbl_client.screenshots.get_saved_own_screenshots(
        skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_saved_own_titleid_filter(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("screenshots_saved_own_titleid")
        )
    )
    ret = await xbl_client.screenshots.get_saved_own_screenshots(
        title_id=219630713, skip_items=0, max_items=25
    )

    assert len(ret.screenshots) == 1

    assert route.called


@pytest.mark.asyncio
async def test_screenshots_saved_community(respx_mock, xbl_client):
    route = respx_mock.get("https://screenshotsmetadata.xboxlive.com").mock(
        return_value=Response(
            200, json=get_response_json("screenshots_saved_community")
        )
    )
    ret = await xbl_client.screenshots.get_saved_community_screenshots_by_title_id(
        219630713
    )

    assert len(ret.screenshots) == 100

    assert route.called
