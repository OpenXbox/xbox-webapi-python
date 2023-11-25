from httpx import AsyncClient, Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_get_title_endpoints(respx_mock, xal_mgr):
    route = respx_mock.get("https://title.mgt.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("auth_title_endpoints"))
    )
    async with AsyncClient() as client:
        await xal_mgr.get_title_endpoints(client)
    assert route.called


@pytest.mark.asyncio
async def test_get_device_token(respx_mock, xal_mgr):
    route = respx_mock.post(
        "https://device.auth.xboxlive.com/device/authenticate"
    ).mock(return_value=Response(200, json=get_response_json("auth_device_token")))
    await xal_mgr.request_device_token()
    assert route.called


@pytest.mark.asyncio
async def test_sisu_authentication(respx_mock, xal_mgr):
    route = respx_mock.post("https://sisu.xboxlive.com/authenticate").mock(
        return_value=Response(
            200,
            json=get_response_json("xal_authentication_resp"),
            headers={"X-SessionId": "abcsession-id"},
        )
    )
    resp, session_id = await xal_mgr.request_sisu_authentication(
        "eyDeviceToken", "code_challenge_string", "state_string"
    )
    assert route.called
    assert session_id == "abcsession-id"
    assert resp.msa_oauth_redirect is not None


@pytest.mark.asyncio
async def test_sisu_authorization(respx_mock, xal_mgr):
    route = respx_mock.post("https://sisu.xboxlive.com/authorize").mock(
        return_value=Response(200, json=get_response_json("xal_authorization_resp"))
    )
    await xal_mgr.do_sisu_authorization(
        "SISU-Session-ID", "eyAccessToken", "eyDeviceToken"
    )
    assert route.called


@pytest.mark.asyncio
async def test_exchange_code_for_token(respx_mock, xal_mgr):
    route = respx_mock.post("https://login.live.com").mock(
        return_value=Response(200, json=get_response_json("auth_oauth2_token"))
    )
    await xal_mgr.exchange_code_for_token("abc", "xyz")

    assert route.called
