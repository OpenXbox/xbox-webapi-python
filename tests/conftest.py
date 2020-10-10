from datetime import datetime, timedelta
import json
import os

from aiohttp import ClientSession
import pytest

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import (
    OAuth2TokenResponse,
    XAUResponse,
    XSTSDisplayClaims,
    XSTSResponse,
)

from tests.common import get_response

collect_ignore = ["setup.py"]


@pytest.fixture(scope="function")
async def auth_mgr(event_loop):
    mgr = AuthenticationManager(
        ClientSession(loop=event_loop), "abc", "123", "http://localhost"
    )
    mgr.oauth = OAuth2TokenResponse.parse_raw(get_response("auth_oauth2_token"))
    mgr.user_token = XAUResponse.parse_raw(get_response("auth_user_token"))
    mgr.xsts_token = XSTSResponse.parse_raw(get_response("auth_xsts_token"))
    return mgr


@pytest.fixture(scope="function")
def xbl_client(auth_mgr):
    return XboxLiveClient(auth_mgr)
