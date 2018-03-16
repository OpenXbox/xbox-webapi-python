"""
Xbox Live Client

Basic factory that stores :class:`XboxLiveLanguage`, User authorization data
and available `Providers`
"""
import logging
import requests

from xbox.webapi.api.provider.eds import EDSProvider
from xbox.webapi.api.provider.lists import ListsProvider
from xbox.webapi.api.provider.gamerpics import GamerpicsProvider
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
            log.error("Xuid was passed in wrong format, neither int nor string")

        self._lang = language

        self.eds = EDSProvider(self)
        self.lists = ListsProvider(self)
        self.gamerpics = GamerpicsProvider(self)

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
