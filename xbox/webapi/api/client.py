"""
Xbox Live Client

Basic factory that stores :class:`XboxLiveLanguage`, User authorization data
and available `Providers`
"""
import logging
from typing import Any

from httpx import Response
from ms_cv import CorrelationVector

from xbox.webapi.api.language import DefaultXboxLiveLanguages, XboxLiveLanguage
from xbox.webapi.api.provider.account import AccountProvider
from xbox.webapi.api.provider.achievements import AchievementsProvider
from xbox.webapi.api.provider.catalog import CatalogProvider
from xbox.webapi.api.provider.cqs import CQSProvider
from xbox.webapi.api.provider.gameclips import GameclipProvider
from xbox.webapi.api.provider.lists import ListsProvider
from xbox.webapi.api.provider.mediahub import MediahubProvider
from xbox.webapi.api.provider.message import MessageProvider
from xbox.webapi.api.provider.people import PeopleProvider
from xbox.webapi.api.provider.presence import PresenceProvider
from xbox.webapi.api.provider.profile import ProfileProvider
from xbox.webapi.api.provider.screenshots import ScreenshotsProvider
from xbox.webapi.api.provider.smartglass import SmartglassProvider
from xbox.webapi.api.provider.titlehub import TitlehubProvider
from xbox.webapi.api.provider.usersearch import UserSearchProvider
from xbox.webapi.api.provider.userstats import UserStatsProvider
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import RateLimitExceededException
from xbox.webapi.common.ratelimits import RateLimit

log = logging.getLogger("xbox.api")


class Session:
    def __init__(self, auth_mgr: AuthenticationManager):
        self._auth_mgr = auth_mgr
        self._cv = CorrelationVector()

    async def request(
        self,
        method: str,
        url: str,
        include_auth: bool = True,
        include_cv: bool = True,
        **kwargs: Any,
    ) -> Response:
        """Proxy Request and add Auth/CV headers."""
        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)

        # Extra, user supplied values
        extra_headers = kwargs.pop("extra_headers", None)
        extra_params = kwargs.pop("extra_params", None)
        extra_data = kwargs.pop("extra_data", None)

        # Rate limit object
        rate_limits: RateLimit = kwargs.pop("rate_limits", None)

        if include_auth:
            # Ensure tokens valid
            await self._auth_mgr.refresh_tokens()
            # Set auth header
            headers[
                "Authorization"
            ] = self._auth_mgr.xsts_token.authorization_header_value

        if include_cv:
            headers["MS-CV"] = self._cv.increment()

        # Extend with optionally supplied values
        if extra_headers:
            headers.update(extra_headers)
        if extra_params:
            # query parameters
            params = params or {}
            params.update(extra_params)
        if extra_data:
            # form encoded post data
            data = data or {}
            data.update(extra_data)

        if rate_limits:
            # Check if rate limits have been exceeded for this endpoint
            if rate_limits.is_exceeded():
                raise RateLimitExceededException("Rate limit exceeded", rate_limits)

        response = await self._auth_mgr.session.request(
            method, url, **kwargs, headers=headers, params=params, data=data
        )

        if rate_limits:
            rate_limits.increment()

        return response

    async def get(self, url: str, **kwargs: Any) -> Response:
        return await self.request("GET", url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> Response:
        return await self.request("OPTIONS", url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> Response:
        return await self.request("HEAD", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Response:
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> Response:
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> Response:
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Response:
        return await self.request("DELETE", url, **kwargs)


class XboxLiveClient:
    def __init__(
        self,
        auth_mgr: AuthenticationManager,
        language: XboxLiveLanguage = DefaultXboxLiveLanguages.United_States,
    ):
        self._auth_mgr = auth_mgr
        self.session = Session(auth_mgr)
        self._language = language

        self.cqs = CQSProvider(self)
        self.lists = ListsProvider(self)
        self.profile = ProfileProvider(self)
        self.achievements = AchievementsProvider(self)
        self.usersearch = UserSearchProvider(self)
        self.gameclips = GameclipProvider(self)
        self.people = PeopleProvider(self)
        self.presence = PresenceProvider(self)
        self.mediahub = MediahubProvider(self)
        self.message = MessageProvider(self)
        self.userstats = UserStatsProvider(self)
        self.screenshots = ScreenshotsProvider(self)
        self.titlehub = TitlehubProvider(self)
        self.account = AccountProvider(self)
        self.catalog = CatalogProvider(self)
        self.smartglass = SmartglassProvider(self)

    @property
    def xuid(self) -> str:
        """
        Gets the Xbox User ID

        Returns: Xbox user Id
        """
        return self._auth_mgr.xsts_token.xuid

    @property
    def language(self) -> XboxLiveLanguage:
        """
        Gets the active Xbox Live Language

        Returns: Active Xbox Live language
        """
        return self._language
