import pytest

from xbox.webapi.api.client import XboxLiveClient


def test_authorization_header(auth_mgr):
    client = XboxLiveClient(auth_mgr)

    assert client.session.headers["Authorization"] == "XBL3.0 x=userhash;token"
