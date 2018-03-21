import io
import os
import pytest
import betamax
from datetime import datetime
from dateutil.tz import tzutc
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.api.client import XboxLiveClient

current_dir = os.path.dirname(__file__)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = os.path.join(current_dir,
                                               'data/cassettes')
    config.default_cassette_options['record_mode'] = 'none'


@pytest.fixture(scope='session')
def jwt():
    return "eyJlSGVsbG9JYW1BVGVzdFRva2VuSnVzdEZvclRoZXNlVW5pdFRlc3Rz" \
           "X0hvcGVmdWxseUFsbFRoZVRlc3RzVHVybk91dEdvb2RfR29vZEx1Y2s="


@pytest.fixture(scope='session')
def token_datetime():
    return datetime(year=2099, month=10, day=11, hour=1, tzinfo=tzutc())


@pytest.fixture(scope='session')
def token_timestring():
    return "2099-10-11T01:00:00.000000Z"


@pytest.fixture(scope='session')
def token_expired_timestring():
    return "2000-10-11T01:00:00.000000Z"


@pytest.fixture(scope='session')
def windows_live_authenticate_response():
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'test_regex.html')
    with io.open(filepath, 'rt') as f:
        html_body = f.read()
    return html_body


@pytest.fixture(scope='session')
def auth_manager():
    return AuthenticationManager()


@pytest.fixture(scope='session')
def xbl_client():
    return XboxLiveClient(
        userhash='012345679',
        auth_token='eyToken==',
        xuid='987654321'
    )
