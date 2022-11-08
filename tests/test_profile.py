from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_profile_by_xuid(respx_mock, xbl_client):
    route = respx_mock.get("https://profile.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("profile_by_xuid"))
    )
    ret = await xbl_client.profile.get_profile_by_xuid("2669321029139235")

    assert len(ret.profile_users) == 1

    assert route.called


@pytest.mark.asyncio
async def test_profile_by_gamertag(respx_mock, xbl_client):
    route = respx_mock.get("https://profile.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("profile_by_gamertag"))
    )
    ret = await xbl_client.profile.get_profile_by_gamertag("e")

    assert len(ret.profile_users) == 1

    assert route.called


@pytest.mark.asyncio
async def test_profiles_batch(respx_mock, xbl_client):
    route = respx_mock.post("https://profile.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("profile_batch"))
    )
    ret = await xbl_client.profile.get_profiles(
        ["2669321029139235", "2584878536129841"]
    )

    assert len(ret.profile_users) == 2

    assert route.called
