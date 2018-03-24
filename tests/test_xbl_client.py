import pytest
from xbox.webapi.api.client import XboxLiveClient


def test_xuid_from_int():
    client = XboxLiveClient('userhash', 'token', 1234567890)

    assert client.xuid == 1234567890


def test_xuid_from_string():
    client = XboxLiveClient('userhash', 'token', '1234567890')

    assert client.xuid == 1234567890


def test_invalid_xuid_format():
    with pytest.raises(ValueError):
        XboxLiveClient('userhash', 'token', b'1234567890')


def test_authorization_header():
    client = XboxLiveClient('userhash', 'token', '1234567890')

    assert client.session.headers['Authorization'] == 'XBL3.0 x=userhash;token'
