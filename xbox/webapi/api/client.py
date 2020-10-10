"""
Xbox Live Client

Basic factory that stores :class:`XboxLiveLanguage`, User authorization data
and available `Providers`
"""
import logging
from typing import Any

from aiohttp import hdrs
from aiohttp.client import ClientResponse
from ms_cv import CorrelationVector

from xbox.webapi.api.language import DefaultXboxLiveLanguages, XboxLiveLanguage
from xbox.webapi.api.provider.account import AccountProvider
from xbox.webapi.api.provider.achievements import AchievementsProvider
from xbox.webapi.api.provider.catalog import CatalogProvider
from xbox.webapi.api.provider.cqs import CQSProvider
from xbox.webapi.api.provider.gameclips import GameclipProvider
from xbox.webapi.api.provider.lists import ListsProvider
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
    ) -> ClientResponse:
        """Proxy Request and add Auth/CV headers."""
        # Ensure tokens valid
        await self._auth_mgr.refresh_tokens()

        # Build request
        headers = kwargs.pop("headers", {})
        if include_auth:
            headers[
                hdrs.AUTHORIZATION
            ] = self._auth_mgr.xsts_token.authorization_header_value
        if include_cv:
            headers["MS-CV"] = self._cv.increment()

        return await self._auth_mgr.session.request(
            method,
            url,
            **kwargs,
            headers=headers,
        )

    async def get(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_GET, url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_OPTIONS, url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_HEAD, url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_POST, url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_PUT, url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_PATCH, url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self.request(hdrs.METH_DELETE, url, **kwargs)


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
