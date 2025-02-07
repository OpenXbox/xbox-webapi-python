from datetime import datetime, timezone
import uuid

from ecdsa.keys import SigningKey, VerifyingKey
import pytest
import pytest_asyncio

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import (
    OAuth2TokenResponse,
    XAUResponse,
    XSTSResponse,
)
from xbox.webapi.authentication.xal import (
    APP_PARAMS_GAMEPASS_BETA,
    CLIENT_PARAMS_ANDROID,
    XALManager,
)
from xbox.webapi.common.request_signer import RequestSigner
from xbox.webapi.common.signed_session import SignedSession

from tests.common import get_response


@pytest_asyncio.fixture(scope="function")
async def auth_mgr():
    session = SignedSession()
    mgr = AuthenticationManager(session, "abc", "123", "http://localhost")
    mgr.oauth = OAuth2TokenResponse.model_validate_json(
        get_response("auth_oauth2_token")
    )
    mgr.user_token = XAUResponse.model_validate_json(get_response("auth_user_token"))
    mgr.xsts_token = XSTSResponse.model_validate_json(get_response("auth_xsts_token"))
    yield mgr
    await session.aclose()


@pytest_asyncio.fixture(scope="function")
async def xal_mgr():
    session = SignedSession()
    mgr = XALManager(
        session,
        device_id=uuid.UUID("9c493431-5462-4a4a-a247-f6420396318d"),
        app_params=APP_PARAMS_GAMEPASS_BETA,
        client_params=CLIENT_PARAMS_ANDROID,
    )
    yield mgr
    await session.aclose()


@pytest.fixture(scope="function")
def xbl_client(auth_mgr):
    return XboxLiveClient(auth_mgr)


@pytest.fixture(scope="session")
def ecdsa_signing_key_str() -> str:
    with open("tests/data/test_signing_key.pem") as f:
        return f.read()


@pytest.fixture(scope="session")
def ecdsa_signing_key(ecdsa_signing_key_str: str) -> SigningKey:
    return SigningKey.from_pem(ecdsa_signing_key_str)


@pytest.fixture(scope="session")
def ecdsa_verifying_key(ecdsa_signing_key: SigningKey) -> VerifyingKey:
    return ecdsa_signing_key.get_verifying_key()


@pytest.fixture(scope="session")
def synthetic_request_signer(ecdsa_signing_key) -> RequestSigner:
    return RequestSigner(ecdsa_signing_key)


@pytest.fixture(scope="session")
def synthetic_timestamp() -> datetime:
    return datetime.fromtimestamp(1586999965, timezone.utc)
