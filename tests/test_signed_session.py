from httpx import Request, Response
import pytest

from xbox.webapi.common.signed_session import SignedSession

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_sending_signed_request(synthetic_request_signer, respx_mock):
    route = respx_mock.post("https://xsts.auth.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("auth_xsts_token"))
    )

    signed_session = SignedSession(synthetic_request_signer)

    request = Request(
        method="POST",
        url="https://xsts.auth.xboxlive.com/xsts/authorize",
        headers={"x-xbl-contract-version": "1"},
        data={
            "RelyingParty": "http://xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": ["eyJWTblabla"],
                "SandboxId": "RETAIL",
            },
        },
    )

    async with signed_session:
        resp = await signed_session.send_request_signed(request)

    assert route.called
    assert resp.request.headers.get("Signature") is not None


@pytest.mark.asyncio
async def test_sending_signed(synthetic_request_signer, respx_mock):
    route = respx_mock.post("https://xsts.auth.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("auth_xsts_token"))
    )

    signed_session = SignedSession(synthetic_request_signer)

    method = "POST"
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    headers = {"x-xbl-contract-version": "1"}
    data = {
        "RelyingParty": "http://xboxlive.com",
        "TokenType": "JWT",
        "Properties": {
            "UserTokens": ["eyJWTblabla"],
            "SandboxId": "RETAIL",
        },
    }

    async with signed_session:
        resp = await signed_session.send_signed(method, url, headers=headers, data=data)

    assert route.called
    assert resp.request.headers.get("Signature") is not None
