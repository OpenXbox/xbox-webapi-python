"""
Authentication Manager

Authenticate with Windows Live Server and Xbox Live.
"""
import aiohttp
import json
import logging
from typing import Any

from yarl import URL

from xbox.webapi.authentication.models import OAuth2TokenResponse, XAUResponse, XSTSResponse

log = logging.getLogger('authentication')


class AuthenticationManager(object):
    def __init__(self, client_session: aiohttp.ClientSession, client_id: str, client_secret: str, redirect_uri: str):
        self.session = client_session
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

        self.oauth: OAuth2TokenResponse = None
        self.user_token: XAUResponse = None
        self.xsts_token: XSTSResponse = None


    def generate_authorization_url(self):
        """
        Generate Windows Live Authorization URL.

        Returns:
            str: Assembled URL, including query parameters
        """
        return str(
            URL("https://login.live.com/oauth20_authorize.srf")
            .with_query(
                {
                    "client_id": self._client_id,
                    "response_type": "code",
                    "approval_prompt": "auto",
                    "scope": "Xboxlive.signin Xboxlive.offline_access",
                    "redirect_uri": self._redirect_uri,
                }
            )
        )


    async def request_tokens(self, authorization_code):
        self.oauth = await self._oauth2_token_request(
            {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "scope": "Xboxlive.signin Xboxlive.offline_access",
                "redirect_uri": self._redirect_uri,
            }
        )
        self.user_token = await self._request_user_token()
        self.xsts_token = await self._request_xsts_token()


    async def refresh_tokens(self):
        self.oauth = await self._oauth2_token_request(
            {
                "grant_type": "refresh_token",
                "scope": "Xboxlive.signin Xboxlive.offline_access",
                "refresh_token": self.oauth.refresh_token,
            }
        )
        self.user_token = await self._request_user_token()
        self.xsts_token = await self._request_xsts_token()


    async def _oauth2_token_request(self, data: dict) -> OAuth2TokenResponse:
        data["client_id"] = self._client_id
        if self._client_secret is not None:
            data["client_secret"] = self._client_secret
        resp = await self.session.post("https://login.live.com/oauth20_token.srf", data=data)
        resp.raise_for_status()
        return OAuth2TokenResponse.parse_raw(await resp.text())


    async def _request_user_token(self) -> XAUResponse:
        """Authenticate via access token and receive user token"""
        url = "https://user.auth.xboxlive.com/user/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d=" + self.oauth.access_token,
            },
        }

        resp = await self.session.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return XAUResponse.parse_raw(await resp.text())


    async def _request_xsts_token(self) -> XSTSResponse:
        """Authorize via user token and receive final X token"""
        url = "https://xsts.auth.xboxlive.com/xsts/authorize"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": [self.user_token.token],
                "SandboxId": "RETAIL",
            },
        }

        resp = await self.session.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return XSTSResponse.parse_raw(await resp.text())
