from httpx import HTTPStatusError, Response
import pytest

from xbox.webapi.api.provider.account.models import (
    ChangeGamertagResult,
    ClaimGamertagResult,
)


@pytest.mark.asyncio
async def test_claim_gamertag(respx_mock, xbl_client):
    route = respx_mock.post("https://user.mgt.xboxlive.com").mock(
        return_value=Response(200)
    )
    ret = await xbl_client.account.claim_gamertag("2669321029139235", "PrettyPony")

    assert ret == ClaimGamertagResult.Available
    assert route.called


@pytest.mark.asyncio
async def test_claim_gamertag_error(respx_mock, xbl_client):
    route = respx_mock.post("https://user.mgt.xboxlive.com").mock(
        return_value=Response(500)
    )
    with pytest.raises(HTTPStatusError) as err:
        await xbl_client.account.claim_gamertag("2669321029139235", "PrettyPony")

    assert err.value.response.status_code == 500
    assert route.called


@pytest.mark.asyncio
async def test_change_gamertag(respx_mock, xbl_client):
    route = respx_mock.post("https://accounts.xboxlive.com").mock(
        return_value=Response(200)
    )
    ret = await xbl_client.account.change_gamertag("2669321029139235", "PrettyPony")

    assert ret == ChangeGamertagResult.ChangeSuccessful
    assert route.called


@pytest.mark.asyncio
async def test_change_gamertag_error(respx_mock, xbl_client):
    route = respx_mock.post("https://accounts.xboxlive.com").mock(
        return_value=Response(500)
    )
    with pytest.raises(HTTPStatusError) as err:
        await xbl_client.account.change_gamertag("2669321029139235", "PrettyPony")

    assert err.value.response.status_code == 500
    assert route.called
