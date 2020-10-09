from aiohttp import ClientResponseError
import pytest

from xbox.webapi.api.provider.account.models import (
    ChangeGamertagResult,
    ClaimGamertagResult,
)


@pytest.mark.asyncio
async def test_claim_gamertag(aresponses, xbl_client):
    aresponses.add(
        "user.mgt.xboxlive.com",
        method_pattern="POST",
        response=aresponses.Response(status=200),
    )
    ret = await xbl_client.account.claim_gamertag("2669321029139235", "PrettyPony")
    await xbl_client._auth_mgr.session.close()

    assert ret == ClaimGamertagResult.Available
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_claim_gamertag_error(aresponses, xbl_client):
    aresponses.add(
        "user.mgt.xboxlive.com",
        method_pattern="POST",
        response=aresponses.Response(status=500),
    )
    with pytest.raises(ClientResponseError) as err:
        await xbl_client.account.claim_gamertag("2669321029139235", "PrettyPony")
    await xbl_client._auth_mgr.session.close()

    assert err.value.code == 500
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_change_gamertag(aresponses, xbl_client):
    aresponses.add(
        "accounts.xboxlive.com",
        method_pattern="POST",
        response=aresponses.Response(status=200),
    )
    ret = await xbl_client.account.change_gamertag("2669321029139235", "PrettyPony")
    await xbl_client._auth_mgr.session.close()

    assert ret == ChangeGamertagResult.ChangeSuccessful
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_change_gamertag_error(aresponses, xbl_client):
    aresponses.add(
        "accounts.xboxlive.com",
        method_pattern="POST",
        response=aresponses.Response(status=500),
    )
    with pytest.raises(ClientResponseError) as err:
        await xbl_client.account.change_gamertag("2669321029139235", "PrettyPony")
    await xbl_client._auth_mgr.session.close()

    assert err.value.code == 500
    aresponses.assert_plan_strictly_followed()
