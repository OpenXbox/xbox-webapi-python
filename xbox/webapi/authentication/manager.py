"""
Authentication Manager

Authenticate with Windows Live Server and Xbox Live.
"""
import logging
from typing import List, Optional

import aiohttp
from yarl import URL

from xbox.webapi.authentication.models import (
    OAuth2TokenResponse,
    XAUResponse,
    XSTSResponse,
)

log = logging.getLogger("authentication")

DEFAULT_SCOPES = ["Xboxlive.signin", "Xboxlive.offline_access"]


class AuthenticationManager:
    def __init__(
        self,
        client_session: aiohttp.ClientSession,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None,
    ):
        self.session: aiohttp.ClientSession = client_session
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_uri: str = redirect_uri
        self._scopes: List[str] = scopes or DEFAULT_SCOPES

        self.oauth: OAuth2TokenResponse = None
        self.user_token: XAUResponse = None
        self.xsts_token: XSTSResponse = None

    def generate_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate Windows Live Authorization URL."""
        query_string = {
            "client_id": self._client_id,
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": " ".join(self._scopes),
            "redirect_uri": self._redirect_uri,
        }

        if state:
            query_string["state"] = state

        return str(
            URL("https://login.live.com/oauth20_authorize.srf").with_query(query_string)
        )

    async def request_tokens(self, authorization_code: str) -> None:
        """Request all tokens."""
        self.oauth = await self.request_oauth_token(authorization_code)
        self.user_token = await self.request_user_token()
        self.xsts_token = await self.request_xsts_token()

    async def refresh_tokens(self) -> None:
        """Refresh all tokens."""
        if not (self.oauth and self.oauth.is_valid()):
            self.oauth = await self.refresh_oauth_token()
        if not (self.user_token and self.user_token.is_valid()):
            self.user_token = await self.request_user_token()
        if not (self.xsts_token and self.xsts_token.is_valid()):
            self.xsts_token = await self.request_xsts_token()

    async def request_oauth_token(self, authorization_code: str) -> OAuth2TokenResponse:
        """Request OAuth2 token."""
        return await self._oauth2_token_request(
            {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "scope": " ".join(self._scopes),
                "redirect_uri": self._redirect_uri,
            }
        )

    async def refresh_oauth_token(self) -> OAuth2TokenResponse:
        """Refresh OAuth2 token."""
        return await self._oauth2_token_request(
            {
                "grant_type": "refresh_token",
                "scope": " ".join(self._scopes),
                "refresh_token": self.oauth.refresh_token,
            }
        )

    async def _oauth2_token_request(self, data: dict) -> OAuth2TokenResponse:
        """Execute token requests."""
        data["client_id"] = self._client_id
        if self._client_secret:
            data["client_secret"] = self._client_secret
        resp = await self.session.post(
            "https://login.live.com/oauth20_token.srf", data=data
        )
        # print(await resp.content.read())
        resp.raise_for_status()
        return OAuth2TokenResponse.parse_raw(await resp.text())

    async def request_user_token(
        self,
        relaying_party: str = "http://auth.xboxlive.com",
        use_compact_ticket: bool = False,
    ) -> XAUResponse:
        """Authenticate via access token and receive user token."""
        url = "https://user.auth.xboxlive.com/user/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": relaying_party,
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": self.oauth.access_token
                if use_compact_ticket
                else f"d={self.oauth.access_token}",
            },
        }

        resp = await self.session.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return XAUResponse.parse_raw(await resp.text())

    async def request_xsts_token(
        self, relaying_party: str = "http://xboxlive.com"
    ) -> XSTSResponse:
        """Authorize via user token and receive final X token."""
        url = "https://xsts.auth.xboxlive.com/xsts/authorize"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": relaying_party,
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": [self.user_token.token],
                "SandboxId": "RETAIL",
            },
        }

        resp = await self.session.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return XSTSResponse.parse_raw(await resp.text())
