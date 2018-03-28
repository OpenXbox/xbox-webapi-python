"""
Presence - Get online status of friends
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class PresenceLevel(object):
    USER = 'user'
    DEVICE = 'device'
    TITLE = 'title'
    ALL = 'all'


class PresenceProvider(BaseProvider):
    PRESENCE_URL = "https://userpresence.xboxlive.com"
    HEADERS_PRESENCE = {
        'x-xbl-contract-version': '3',
        'Accept': 'application/json'
    }

    def get_presence_batch(self, xuids, online_only=False, presence_level=PresenceLevel.USER):
        """
        Get presence for list of xuids

        Args:
            xuids (str): List of XUIDs
            online_only (bool): Only get online profiles
            presence_level (str): Filter level

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(xuids, list):
            raise Exception("xuids parameter is not a list")
        elif len(xuids) > 1100:
            raise Exception("Xuid list length is > 1100")

        url = self.PRESENCE_URL + "/users/batch"
        post_data = {
            'users': [str(x) for x in xuids],
            'onlineOnly': online_only,
            'level': presence_level
        }
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_PRESENCE)

    def get_presence_own(self, presence_level=PresenceLevel.ALL):
        """
        Get presence of own profile

        Args:
            presence_level (str): Filter level

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.PRESENCE_URL + "/users/me"
        params = {
            'level': presence_level
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_PRESENCE)
