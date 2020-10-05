"""
Xbox Live Client

Basic factory that stores :class:`XboxLiveLanguage`, User authorization data
and available `Providers`
"""
import logging
from typing import Any

from aiohttp import hdrs
from aiohttp.client import ClientResponse

from xbox.webapi.api.language import DefaultXboxLiveLocales, XboxLiveLocale
from xbox.webapi.api.provider.account import AccountProvider
from xbox.webapi.api.provider.achievements import AchievementsProvider
from xbox.webapi.api.provider.cqs import CQSProvider
from xbox.webapi.api.provider.eds import EDSProvider
from xbox.webapi.api.provider.gameclips import GameclipProvider
from xbox.webapi.api.provider.lists import ListsProvider
from xbox.webapi.api.provider.message import MessageProvider
from xbox.webapi.api.provider.people import PeopleProvider
from xbox.webapi.api.provider.presence import PresenceProvider
from xbox.webapi.api.provider.profile import ProfileProvider
from xbox.webapi.api.provider.screenshots import ScreenshotsProvider
from xbox.webapi.api.provider.titlehub import TitlehubProvider
from xbox.webapi.api.provider.usersearch import UserSearchProvider
from xbox.webapi.api.provider.userstats import UserStatsProvider
from xbox.webapi.authentication.manager import AuthenticationManager

log = logging.getLogger("xbox.api")


class Session:
    def __init__(self, auth_mgr: AuthenticationManager):
        self._auth_mgr = auth_mgr

    async def request(self, method: str, url: str, **kwargs: Any) -> ClientResponse:
        headers = kwargs.pop("headers", {})
        resp = await self._auth_mgr.session.request(
            method,
            url,
            **kwargs,
            headers={
                hdrs.AUTHORIZATION: self._auth_mgr.xsts_token.authorization_header_value,
                **headers,
            },
        )
        return resp

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
        locale: XboxLiveLocale = DefaultXboxLiveLocales.United_States,
    ):
        self._auth_mgr = auth_mgr
        self.session = Session(auth_mgr)
        self._locale = locale

        self.eds = EDSProvider(self)
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

    @property
    def xuid(self) -> str:
        """
        Gets the Xbox User ID

        Returns: Xbox user Id
        """
        return self._auth_mgr.xsts_token.xuid

    @property
    def locale(self) -> XboxLiveLocale:
        """
        Gets the active Xbox Live Locale

        Returns: Active Xbox Live locale
        """
        return self._locale
