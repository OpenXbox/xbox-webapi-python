import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_gameclips_recent_xuid(aresponses, xbl_client):
    aresponses.add("eplists.xboxlive.com", response=get_response("lists_get_items"))
    ret = await xbl_client.lists.get_items(xbl_client.xuid)
    await xbl_client._auth_mgr.session.close()

    assert ret.list_metadata.list_count == 3
    aresponses.assert_plan_strictly_followed()
