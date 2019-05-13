"""
Xbox Live Client

Basic factory that stores :class:`XboxLiveLanguage`, User authorization data
and available `Providers`
"""
import logging
import requests

from xbox.webapi.api.provider.eds import EDSProvider
from xbox.webapi.api.provider.cqs import CQSProvider
from xbox.webapi.api.provider.lists import ListsProvider
from xbox.webapi.api.provider.profile import ProfileProvider
from xbox.webapi.api.provider.achievements import AchievementsProvider
from xbox.webapi.api.provider.usersearch import UserSearchProvider
from xbox.webapi.api.provider.gameclips import GameclipProvider
from xbox.webapi.api.provider.people import PeopleProvider
from xbox.webapi.api.provider.presence import PresenceProvider
from xbox.webapi.api.provider.message import MessageProvider
from xbox.webapi.api.provider.userstats import UserStatsProvider
from xbox.webapi.api.provider.screenshots import ScreenshotsProvider
from xbox.webapi.api.provider.titlehub import TitlehubProvider
from xbox.webapi.api.provider.account import AccountProvider
from xbox.webapi.api.language import XboxLiveLanguage

log = logging.getLogger('xbox.api')


class XboxLiveClient(object):
    def __init__(self, userhash, auth_token, xuid, language=XboxLiveLanguage.United_States):
        """
        Provide various Web API from Xbox Live

        Args:
            userhash (str): Userhash obtained by authentication with Xbox Live Server
            auth_token (str): Authentication Token (XSTS), obtained by authentication with Xbox Live Server
            xuid (str/int): Xbox User Identification of your Xbox Live Account
            language (str): Member of :class:`XboxLiveLanguage`
        """
        authorization_header = {'Authorization': 'XBL3.0 x=%s;%s' % (userhash, auth_token)}

        self._session = requests.session()
        self._session.headers.update(authorization_header)  # Set authorization header for whole session

        if isinstance(xuid, str):
            self._xuid = int(xuid)
        elif isinstance(xuid, int):
            self._xuid = xuid
        else:
            raise ValueError("Xuid was passed in wrong format, neither int nor string")

        self._lang = language

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
    def xuid(self):
        """
        Gets the Xbox User ID

        Returns:
            int: Xbox User ID
        """
        return self._xuid

    @property
    def language(self):
        """
        Gets the active Xbox Live Language

        Returns:
            :class:`XboxLiveLanguage`: Active Xbox Live language
        """
        return self._lang

    @property
    def session(self):
        """
        Wrapper around requests session

        Returns:
            object: Instance of :class:`requests.session` - Xbox Live Authorization header is set.
        """
        return self._session
