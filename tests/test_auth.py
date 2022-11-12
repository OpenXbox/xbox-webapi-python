from datetime import datetime, timedelta, timezone

from httpx import Response
import pytest

from tests.common import get_response_json


@pytest.mark.asyncio
async def test_generate_auth_url(auth_mgr):
    url = auth_mgr.generate_authorization_url()
    assert url.startswith("https://login.live.com/oauth20_authorize.srf?")
    assert "client_id=abc" in url
    assert "response_type=code" in url


@pytest.mark.asyncio
async def test_generate_auth_url_with_state(auth_mgr):
    state = "test_state"
    url = auth_mgr.generate_authorization_url(state)
    assert f"state={state}" in url


@pytest.mark.asyncio
async def test_request_tokens(respx_mock, auth_mgr):
    route1 = respx_mock.post("https://login.live.com").mock(
        return_value=Response(200, json=get_response_json("auth_oauth2_token"))
    )
    route2 = respx_mock.post("https://user.auth.xboxlive.com/user/authenticate").mock(
        return_value=Response(200, json=get_response_json("auth_user_token"))
    )
    route3 = respx_mock.post("https://xsts.auth.xboxlive.com/xsts/authorize").mock(
        return_value=Response(200, json=get_response_json("auth_xsts_token"))
    )
    await auth_mgr.request_tokens("CODE")
    assert route1.called
    assert route2.called
    assert route3.called


@pytest.mark.asyncio
async def test_refresh_tokens(respx_mock, auth_mgr):
    # Expire Tokens
    expired = datetime.now(timezone.utc) - timedelta(days=10)
    auth_mgr.oauth.issued = expired
    auth_mgr.user_token.not_after = expired
    auth_mgr.xsts_token.not_after = expired

    route1 = respx_mock.post("https://login.live.com").mock(
        return_value=Response(200, json=get_response_json("auth_oauth2_token"))
    )
    route2 = respx_mock.post("https://user.auth.xboxlive.com/user/authenticate").mock(
        return_value=Response(200, json=get_response_json("auth_user_token"))
    )
    route3 = respx_mock.post("https://xsts.auth.xboxlive.com/xsts/authorize").mock(
        return_value=Response(200, json=get_response_json("auth_xsts_token"))
    )
    await auth_mgr.refresh_tokens()
    assert route1.called
    assert route2.called
    assert route3.called


@pytest.mark.asyncio
async def test_refresh_tokens_still_valid(auth_mgr):
    now = datetime.now(timezone.utc)
    auth_mgr.oauth.issued = now
    auth_mgr.user_token.not_after = now + timedelta(days=1)
    auth_mgr.xsts_token.not_after = now + timedelta(days=1)
    await auth_mgr.refresh_tokens()


@pytest.mark.asyncio
async def test_refresh_tokens_user_still_valid(respx_mock, auth_mgr):
    # Expire Tokens
    expired = datetime.now(timezone.utc) - timedelta(days=10)
    auth_mgr.oauth.issued = expired
    auth_mgr.xsts_token.not_after = expired

    auth_mgr.user_token.not_after = datetime.now(timezone.utc) + timedelta(days=1)
    route1 = respx_mock.post("https://login.live.com").mock(
        return_value=Response(200, json=get_response_json("auth_oauth2_token"))
    )
    route2 = respx_mock.post("https://xsts.auth.xboxlive.com/xsts/authorize").mock(
        return_value=Response(200, json=get_response_json("auth_xsts_token"))
    )
    await auth_mgr.refresh_tokens()
    assert route1.called
    assert route2.called


@pytest.mark.asyncio
async def test_xsts_properties(auth_mgr):
    assert auth_mgr.xsts_token.xuid == "2669321029139235"
    assert auth_mgr.xsts_token.gamertag == "e"
    assert auth_mgr.xsts_token.userhash == "abcdefg"
    assert auth_mgr.xsts_token.age_group == "Adult"
    assert auth_mgr.xsts_token.privileges == ""
    assert auth_mgr.xsts_token.user_privileges == ""
