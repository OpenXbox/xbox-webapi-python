import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_profile_by_xuid(aresponses, xbl_client):
    aresponses.add(
        "usersearch.xboxlive.com", response=get_response("usersearch_live_search")
    )
    ret = await xbl_client.usersearch.get_live_search("tux")
    await xbl_client._auth_mgr.session.close()

    assert len(ret.results) == 8

    aresponses.assert_plan_strictly_followed()
