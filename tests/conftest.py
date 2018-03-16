import io
import os
import pytest
from datetime import datetime
from dateutil.tz import tzutc
from xbox.webapi.authentication.manager import AuthenticationManager


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
