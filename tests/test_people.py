import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_people_friends_own(aresponses, xbl_client):
    aresponses.add("social.xboxlive.com", response=get_response("people_friends_own"))
    ret = await xbl_client.people.get_friends_own()
    await xbl_client._auth_mgr.session.close()

    assert ret.total_count == 2
    assert len(ret.people) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_people_summary_by_gamertag(aresponses, xbl_client):
    aresponses.add(
        "social.xboxlive.com", response=get_response("people_summary_by_gamertag")
    )
    ret = await xbl_client.people.get_friends_summary_by_gamertag("e")
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_people_summary_by_xuid(aresponses, xbl_client):
    aresponses.add(
        "social.xboxlive.com", response=get_response("people_summary_by_xuid")
    )
    ret = await xbl_client.people.get_friends_summary_by_xuid("2669321029139235")
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_people_summary_own(aresponses, xbl_client):
    aresponses.add("social.xboxlive.com", response=get_response("people_summary_own"))
    ret = await xbl_client.people.get_friends_summary_own()
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_profiles_batch(aresponses, xbl_client):
    aresponses.add("social.xboxlive.com", response=get_response("people_batch"))
    ret = await xbl_client.people.get_friends_own_batch(
        ["2669321029139235", "2584878536129841"]
    )
    await xbl_client._auth_mgr.session.close()

    assert ret.total_count == 2
    assert len(ret.people) == 2

    aresponses.assert_plan_strictly_followed()
