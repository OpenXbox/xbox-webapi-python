import pytest

from xbox.webapi.api.client import XboxLiveClient


def test_authorization_header(auth_mgr):
    client = XboxLiveClient(auth_mgr)

    assert (
        client._auth_mgr.xsts_token.authorization_header_value
        == "XBL3.0 x=abcdefg;123456789"
    )
