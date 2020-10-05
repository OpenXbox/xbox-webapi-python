import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_profile_by_xuid(aresponses, xbl_client):
    aresponses.add("profile.xboxlive.com", response=get_response("profile_by_xuid"))
    ret = await xbl_client.profile.get_profile_by_xuid("2669321029139235")
    await xbl_client._auth_mgr.session.close()

    assert len(ret.profile_users) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_profile_by_gamertag(aresponses, xbl_client):
    aresponses.add("profile.xboxlive.com", response=get_response("profile_by_gamertag"))
    ret = await xbl_client.profile.get_profile_by_gamertag("e")
    await xbl_client._auth_mgr.session.close()

    assert len(ret.profile_users) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_profiles_batch(aresponses, xbl_client):
    aresponses.add("profile.xboxlive.com", response=get_response("profile_batch"))
    ret = await xbl_client.profile.get_profiles(
        ["2669321029139235", "2584878536129841"]
    )
    await xbl_client._auth_mgr.session.close()

    assert len(ret.profile_users) == 2

    aresponses.assert_plan_strictly_followed()
