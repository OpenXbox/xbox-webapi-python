import os
import json
import pytest
import betamax
from datetime import datetime
from xbox.webapi.api.client import XboxLiveClient

current_dir = os.path.dirname(__file__)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = os.path.join(current_dir,
                                               'data/cassettes')
    config.default_cassette_options['record_mode'] = 'none'


@pytest.fixture(scope='session')
def redirect_url():
    return "https://login.live.com/oauth20_desktop.srf?lc=1033#access_token=AccessToken&token_type=bearer&" \
           "expires_in=86400&scope=service::user.auth.xboxlive.com::MBI_SSL&refresh_token=RefreshToken&" \
           "user_id=1005283eaccf208b"


@pytest.fixture(scope='session')
def jwt():
    return "eyJlSGVsbG9JYW1BVGVzdFRva2VuSnVzdEZvclRoZXNlVW5pdFRlc3Rz" \
           "X0hvcGVmdWxseUFsbFRoZVRlc3RzVHVybk91dEdvb2RfR29vZEx1Y2s="


@pytest.fixture(scope='session')
def token_datetime():
    return datetime(year=2099, month=10, day=11, hour=1)


@pytest.fixture(scope='session')
def token_timestring():
    return "2099-10-11T01:00:00.000000Z"


@pytest.fixture(scope='session')
def token_expired_timestring():
    return "2000-10-11T01:00:00.000000Z"


@pytest.fixture(scope='session')
def windows_live_authenticate_response():
    filepath = os.path.join(current_dir, 'data', 'wl_auth_response.html')
    with open(filepath, 'r') as f:
        return f.read()

@pytest.fixture(scope='session')
def windows_live_authenticate_response_two_js_obj():
    filepath = os.path.join(current_dir, 'data', 'wl_auth_response_two_js_obj.html')
    with open(filepath, 'r') as f:
        return f.read()


@pytest.fixture(scope='session')
def tokens_filepath():
    filepath = os.path.join(current_dir, 'data', 'tokens.json')
    return filepath


@pytest.fixture(scope='session')
def tokens_json(tokens_filepath):
    with open(tokens_filepath, 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session')
def xbl_client():
    return XboxLiveClient(
        userhash='012345679',
        auth_token='eyToken==',
        xuid='987654321'
    )
