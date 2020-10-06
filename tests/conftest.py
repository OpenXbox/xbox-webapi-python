from datetime import datetime, timedelta
import json
import os

from aiohttp import ClientSession
import pytest

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import XSTSDisplayClaims, XSTSResponse

collect_ignore = ["setup.py"]


@pytest.fixture(scope="function")
async def auth_mgr(event_loop):
    mgr = AuthenticationManager(
        ClientSession(loop=event_loop), "abc", "123", "http://localhost"
    )
    mgr.xsts_token = XSTSResponse(
        issue_instant=datetime.utcnow(),
        not_after=datetime.utcnow() + timedelta(hours=16),
        token="123456789",
        display_claims=XSTSDisplayClaims(
            xui=[{"xid": "2669321029139235", "uhs": "abcdefg"}]
        ),
    )
    return mgr


@pytest.fixture(scope="function")
def xbl_client(auth_mgr):
    return XboxLiveClient(auth_mgr)
