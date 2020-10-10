from datetime import datetime, timedelta, timezone

import pytest

from tests.common import get_response


@pytest.mark.asyncio
async def test_generate_auth_url(auth_mgr):
    url = auth_mgr.generate_authorization_url()
    assert "https://login.live.com/oauth20_authorize.srf" in url


@pytest.mark.asyncio
async def test_generate_auth_url_with_state(auth_mgr):
    state = "test_state"
    url = auth_mgr.generate_authorization_url(state)
    assert f"state={state}" in url


@pytest.mark.asyncio
async def test_request_tokens(aresponses, auth_mgr):
    aresponses.add("login.live.com", response=get_response("auth_oauth2_token"))
    aresponses.add(
        "user.auth.xboxlive.com",
        "/user/authenticate",
        response=get_response("auth_user_token"),
    )
    aresponses.add(
        "xsts.auth.xboxlive.com",
        "/xsts/authorize",
        response=get_response("auth_xsts_token"),
    )
    await auth_mgr.request_tokens("CODE")
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_refresh_tokens(aresponses, auth_mgr):
    aresponses.add("login.live.com", response=get_response("auth_oauth2_token"))
    aresponses.add(
        "user.auth.xboxlive.com",
        "/user/authenticate",
        response=get_response("auth_user_token"),
    )
    aresponses.add(
        "xsts.auth.xboxlive.com",
        "/xsts/authorize",
        response=get_response("auth_xsts_token"),
    )
    await auth_mgr.refresh_tokens()
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_refresh_tokens_still_valid(aresponses, auth_mgr):
    now = datetime.now(timezone.utc)
    auth_mgr.oauth.issued = now
    auth_mgr.user_token.not_after = now + timedelta(days=1)
    auth_mgr.xsts_token.not_after = now + timedelta(days=1)
    await auth_mgr.refresh_tokens()
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_refresh_tokens_user_still_valid(aresponses, auth_mgr):
    auth_mgr.user_token.not_after = datetime.now(timezone.utc) + timedelta(days=1)
    aresponses.add("login.live.com", response=get_response("auth_oauth2_token"))
    aresponses.add(
        "xsts.auth.xboxlive.com",
        "/xsts/authorize",
        response=get_response("auth_xsts_token"),
    )
    await auth_mgr.refresh_tokens()
    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_xsts_properties(auth_mgr):
    assert auth_mgr.xsts_token.xuid == "2669321029139235"
    assert auth_mgr.xsts_token.gamertag == "e"
    assert auth_mgr.xsts_token.userhash == "abcdefg"
    assert auth_mgr.xsts_token.age_group == "Adult"
    assert auth_mgr.xsts_token.privileges == ""
    assert auth_mgr.xsts_token.user_privileges == ""
