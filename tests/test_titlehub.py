import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_titlehub_titlehistory(aresponses, xbl_client):
    aresponses.add(
        "titlehub.xboxlive.com", response=get_response("titlehub_titlehistory")
    )
    ret = await xbl_client.titlehub.get_title_history(987654321)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.titles) == 5

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_titlehub_titleinfo(aresponses, xbl_client):
    aresponses.add("titlehub.xboxlive.com", response=get_response("titlehub_titleinfo"))
    ret = await xbl_client.titlehub.get_title_info(1717113201)
    await xbl_client._auth_mgr.session.close()

    assert len(ret.titles) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_titlehub_batch(aresponses, xbl_client):
    aresponses.add("titlehub.xboxlive.com", response=get_response("titlehub_batch"))
    ret = await xbl_client.titlehub.get_titles_batch(
        ["Microsoft.SeaofThieves_8wekyb3d8bbwe", "Microsoft.XboxApp_8wekyb3d8bbwe"]
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.titles) == 2

    aresponses.assert_plan_strictly_followed()
