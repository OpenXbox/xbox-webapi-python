import pytest

from xbox.webapi.api.provider import eds
from xbox.webapi.api.provider.eds.models import MediaItemType

from tests.common import get_response


@pytest.mark.asyncio
async def test_get_details(aresponses, xbl_client):
    aresponses.add("eds.xboxlive.com", response=get_response("eds_get_details"))
    ret = await xbl_client.eds.get_details(
        ids=[
            "a3807603-9e22-48b2-8b75-c6bf36ddc511",
            "e0dec6f3-9e8f-4f0c-a93a-acfba29fd890",
        ],
        mediagroup=eds.MediaGroup.GAME_TYPE,
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.items) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_singlemediagroup_search(aresponses, xbl_client):
    aresponses.add(
        "eds.xboxlive.com", response=get_response("eds_singlemediagroup_search")
    )
    ret = await xbl_client.eds.get_singlemediagroup_search(
        search_query="sea", max_items=1, media_item_types=[MediaItemType.XBOXONE_GAME]
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.items) == 1
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_crossmediagroup_search(aresponses, xbl_client):
    aresponses.add(
        "eds.xboxlive.com", response=get_response("eds_crossmediagroup_search")
    )
    ret = await xbl_client.eds.get_crossmediagroup_search(
        search_query="halo", max_items=10
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.items) == 10
    aresponses.assert_plan_strictly_followed()
