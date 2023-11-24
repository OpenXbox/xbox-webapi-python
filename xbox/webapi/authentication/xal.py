"""
Xbox Authentication Library

Authenticate with Windows Live Server and Xbox Live (used by mobile Xbox Apps)
"""
import base64
import hashlib
import logging
import os
from typing import Callable, Tuple
from urllib import parse
import uuid

import httpx
from ms_cv import CorrelationVector

from xbox.webapi.authentication.models import (
    OAuth2TokenResponse,
    SisuAuthenticationResponse,
    SisuAuthorizationResponse,
    TitleEndpointsResponse,
    XADResponse,
    XalAppParameters,
    XalClientParameters,
    XSTSResponse,
)
from xbox.webapi.common.signed_session import SignedSession

log = logging.getLogger("xal.authentication")

APP_PARAMS_XBOX_BETA_APP = XalAppParameters(
    app_id="000000004415494b",
    title_id="177887386",
    redirect_uri="ms-xal-000000004415494b://auth",
)

APP_PARAMS_XBOX_APP = XalAppParameters(
    app_id="000000004c12ae6f",
    title_id="328178078",
    redirect_uri="ms-xal-000000004c12ae6f://auth",
)

APP_PARAMS_GAMEPASS = XalAppParameters(
    app_id="000000004c20a908",
    title_id="1016898439",
    redirect_uri="ms-xal-000000004c20a908://auth",
)

APP_PARAMS_GAMEPASS_BETA = XalAppParameters(
    app_id="000000004c20a908",
    title_id="1016898439",
    redirect_uri="ms-xal-public-beta-000000004c20a908://auth",
)

APP_PARAMS_FAMILY_SETTINGS = XalAppParameters(
    app_id="00000000482C8F49",
    title_id="1618633878",
    redirect_uri="https://login.live.com/oauth20_desktop.srf",
)

CLIENT_PARAMS_IOS = XalClientParameters(
    user_agent="XAL iOS 2021.11.20211021.000",
    device_type="iOS",
    client_version="15.6.1",
    query_display="ios_phone",
)

CLIENT_PARAMS_ANDROID = XalClientParameters(
    user_agent="XAL Android 2020.07.20200714.000",
    device_type="Android",
    client_version="8.0.0",
    query_display="android_phone",
)


class XALManager:
    def __init__(
        self,
        session: SignedSession,
        device_id: uuid.UUID,
        app_params: XalAppParameters,
        client_params: XalClientParameters,
    ):
        self.session = session
        self.device_id = device_id
        self.app_params = app_params
        self.client_params = client_params
        self.cv = CorrelationVector()

    @staticmethod
    def _get_random_bytes(length) -> bytes:
        return os.urandom(length)

    @staticmethod
    def _generate_code_verifier() -> str:
        # https://tools.ietf.org/html/rfc7636
        code_verifier = (
            base64.urlsafe_b64encode(XALManager._get_random_bytes(32))
            .decode()
            .rstrip("=")
        )
        assert len(code_verifier) >= 43 and len(code_verifier) <= 128

        return code_verifier

    @staticmethod
    def _get_code_challenge_from_code_verifier(code_verifier: str) -> str:
        code_challenge = hashlib.sha256(code_verifier.encode()).digest()
        # Base64 urlsafe encoding WITH stripping trailing '='
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode().rstrip("=")

        return code_challenge

    @staticmethod
    def _generate_random_state() -> str:
        state = str(uuid.uuid4()).encode()
        # Base64 urlsafe encoding WITHOUT stripping trailing '='
        return base64.b64encode(state).decode()

    @staticmethod
    async def get_title_endpoints(session: httpx.AsyncClient) -> TitleEndpointsResponse:
        url = "https://title.mgt.xboxlive.com/titles/default/endpoints"
        headers = {"x-xbl-contract-version": "1"}
        params = {"type": 1}
        resp = await session.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return TitleEndpointsResponse(**resp.json())

    async def request_device_token(self) -> XADResponse:
        # Proof of possession: https://tools.ietf.org/html/rfc7800

        device_id = str(self.device_id)

        if self.client_params.device_type.lower() == "android":
            # {decf45e4-945d-4379-b708-d4ee92c12d99}
            device_id = "{%s}" % device_id
        else:
            # iOSs
            # DECF45E4-945D-4379-B708-D4EE92C12D99
            device_id = device_id.upper()

        url = "https://device.auth.xboxlive.com/device/authenticate"
        headers = {"x-xbl-contract-version": "1", "MS-CV": self.cv.get_value()}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "ProofOfPossession",
                "Id": device_id,
                "DeviceType": self.client_params.device_type,
                "Version": self.client_params.client_version,
                "ProofKey": self.session.request_signer.proof_field,
            },
        }

        resp = await self.session.send_signed("POST", url, headers=headers, json=data)
        resp.raise_for_status()
        return XADResponse(**resp.json())

    async def __oauth20_token_endpoint(self, json_body: dict) -> httpx.Response:
        url = "https://login.live.com/oauth20_token.srf"
        headers = {"MS-CV": self.cv.increment()}

        # NOTE: No signature necessary
        return await self.session.post(url, headers=headers, data=json_body)

    async def exchange_code_for_token(
        self, authorization_code: str, code_verifier: str
    ) -> OAuth2TokenResponse:
        post_body = {
            "client_id": self.app_params.app_id,
            "code": authorization_code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": self.app_params.redirect_uri,
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
        }
        resp = await self.__oauth20_token_endpoint(post_body)
        resp.raise_for_status()
        return OAuth2TokenResponse(**resp.json())

    async def refresh_token(self, refresh_token_jwt: str) -> httpx.Response:
        post_body = {
            "client_id": self.app_params.app_id,
            "refresh_token": refresh_token_jwt,
            "grant_type": "refresh_token",
            "redirect_uri": self.app_params.redirect_uri,
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
        }

        resp = await self.__oauth20_token_endpoint(post_body)
        resp.raise_for_status()
        return resp

    async def request_sisu_authentication(
        self, device_token_jwt: str, code_challenge: str, state: str
    ) -> Tuple[SisuAuthenticationResponse, str]:
        """
        Request Sisu authentication URL

        Response holds authentication URL that needs to be called by the user
        in webbrowser

        Returns:
            Tuple of (authentication response, sisu session id)
        """
        url = "https://sisu.xboxlive.com/authenticate"
        headers = {"x-xbl-contract-version": "1", "MS-CV": self.cv.increment()}
        post_body = {
            "AppId": self.app_params.app_id,
            "TitleId": self.app_params.title_id,
            "RedirectUri": self.app_params.redirect_uri,
            "DeviceToken": device_token_jwt,
            "Sandbox": "RETAIL",
            "TokenType": "code",
            "Offers": ["service::user.auth.xboxlive.com::MBI_SSL"],
            "Query": {
                "display": self.client_params.query_display,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
                "state": state,
            },
        }

        resp = await self.session.send_signed(
            "POST", url, headers=headers, json=post_body
        )
        resp.raise_for_status()
        return (
            SisuAuthenticationResponse.model_validate_json(resp.content),
            resp.headers["X-SessionId"],
        )

    async def do_sisu_authorization(
        self, sisu_session_id: str, access_token_jwt: str, device_token_jwt: str
    ) -> SisuAuthorizationResponse:
        """
        Sisu authorization

        Returns:
            Response with device-/title-/user-tokens
        """
        url = "https://sisu.xboxlive.com/authorize"
        headers = {"MS-CV": self.cv.increment()}
        post_body = {
            "AccessToken": f"t={access_token_jwt}",
            "AppId": self.app_params.app_id,
            "DeviceToken": device_token_jwt,
            "Sandbox": "RETAIL",
            "SiteName": "user.auth.xboxlive.com",
            "SessionId": sisu_session_id,
            "ProofKey": self.session.request_signer.proof_field,
        }

        resp = await self.session.send_signed(
            "POST", url, headers=headers, json=post_body
        )
        resp.raise_for_status()
        return SisuAuthorizationResponse(**resp.json())

    async def xsts_authorization(
        self,
        device_token_jwt: str,
        title_token_jwt: str,
        user_token_jwt: str,
        relying_party: str,
    ) -> XSTSResponse:
        """
        Request additional XSTS tokens for specific relying parties
        """
        url = "https://xsts.auth.xboxlive.com/xsts/authorize"
        headers = {"x-xbl-contract-version": "1", "MS-CV": self.cv.increment()}
        post_body = {
            "RelyingParty": relying_party,
            "TokenType": "JWT",
            "Properties": {
                "SandboxId": "RETAIL",
                "DeviceToken": device_token_jwt,
                "TitleToken": title_token_jwt,
                "UserTokens": [user_token_jwt],
            },
        }

        resp = await self.session.send_signed(
            "POST", url, headers=headers, json=post_body
        )
        resp.raise_for_status()
        return XSTSResponse(**resp.json())

    async def auth_flow(
        self, user_input_cb: Callable[[str], str]
    ) -> SisuAuthorizationResponse:
        """
        Does the whole XAL/Sisu authentication flow

        Args:
            user_input_cb: User callback which takes args: (auth_url: str) and
                returns the redirect URL (str)

        Returns:
            Sisu authorization response with all tokens
        """

        # Fetch device token
        device_token_resp = await self.request_device_token()

        # Generate states for OAUTH
        code_verifier = self._generate_code_verifier()
        code_challenge = self._get_code_challenge_from_code_verifier(code_verifier)
        state = self._generate_random_state()

        # Request Sisu authentication URL
        (
            sisu_authenticate_resp,
            sisu_session_id,
        ) = await self.request_sisu_authentication(
            device_token_resp.token, code_challenge, state
        )

        # Prompt user for redirect URI after auth
        redirect_uri = user_input_cb(sisu_authenticate_resp.msa_oauth_redirect)

        # Ensure redirect URI looks like expected
        if not redirect_uri.startswith(self.app_params.redirect_uri):
            raise Exception("Wrong data passed as redirect URI")

        # Parse URL query
        query_params = dict(parse.parse_qsl(parse.urlsplit(redirect_uri).query))

        # Extract code and state
        resp_authorization_code = query_params["code"]
        resp_state = query_params["state"]

        if resp_state != state:
            raise Exception("Response with non-matching state received")

        # Exchange authentication code for tokens
        tokens = await self.exchange_code_for_token(
            resp_authorization_code, code_verifier
        )

        # Do Sisu authorization
        sisu_authorization = await self.do_sisu_authorization(
            sisu_session_id, tokens.access_token, device_token_resp.token
        )

        return sisu_authorization
