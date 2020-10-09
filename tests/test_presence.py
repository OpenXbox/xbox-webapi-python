import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_presence_batch(aresponses, xbl_client):
    aresponses.add("userpresence.xboxlive.com", response=get_response("presence_batch"))
    ret = await xbl_client.presence.get_presence_batch(
        ["2669321029139235", "2584878536129841"]
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_presence_too_many_people(xbl_client):
    xuids = range(0, 2000)
    with pytest.raises(Exception) as err:
        await xbl_client.presence.get_presence_batch(xuids)

    assert "length is > 1100" in str(err)
    await xbl_client._auth_mgr.session.close()


@pytest.mark.asyncio
async def test_presence_own(aresponses, xbl_client):
    aresponses.add("userpresence.xboxlive.com", response=get_response("presence_own"))
    ret = await xbl_client.presence.get_presence_own()
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()
