import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_people_friends_own(aresponses, xbl_client):
    aresponses.add(
        "peoplehub.xboxlive.com", response=get_response("people_friends_own")
    )
    ret = await xbl_client.people.get_friends_own()
    await xbl_client._auth_mgr.session.close()

    assert len(ret.people) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_people_friends_by_xuid(aresponses, xbl_client):
    aresponses.add(
        "peoplehub.xboxlive.com", response=get_response("people_friends_by_xuid")
    )
    ret = await xbl_client.people.get_friends_by_xuid("2669321029139235")
    await xbl_client._auth_mgr.session.close()

    assert len(ret.people) == 2
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_profiles_batch(aresponses, xbl_client):
    aresponses.add("peoplehub.xboxlive.com", response=get_response("people_batch"))
    ret = await xbl_client.people.get_friends_own_batch(
        ["271958441785640", "277923030577271", "266932102913935"]
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.people) == 3

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_people_recommendations(aresponses, xbl_client):
    aresponses.add(
        "peoplehub.xboxlive.com", response=get_response("people_recommendations")
    )
    ret = await xbl_client.people.get_friend_recommendations()
    await xbl_client._auth_mgr.session.close()

    assert ret.recommendation_summary.friend_of_friend == 20
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_people_summary_own(aresponses, xbl_client):
    aresponses.add("social.xboxlive.com", response=get_response("people_summary_own"))
    ret = await xbl_client.people.get_friends_summary_own()
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
async def test_people_summary_by_gamertag(aresponses, xbl_client):
    aresponses.add(
        "social.xboxlive.com", response=get_response("people_summary_by_gamertag")
    )
    ret = await xbl_client.people.get_friends_summary_by_gamertag("e")
    await xbl_client._auth_mgr.session.close()

    aresponses.assert_plan_strictly_followed()
