"""
People - Access friendlist from own profiles and others
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class PeopleProvider(BaseProvider):
    SOCIAL_URL = "https://social.xboxlive.com"
    HEADERS_SOCIAL = {'x-xbl-contract-version': '1'}

    async def get_friends_own(self):
        """
        Get friendlist of own profile

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/me/people"
        return await self.client.session.get(url, headers=self.HEADERS_SOCIAL)

    async def get_friends_summary_own(self):
        """
        Get friendlist summary of own profile

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/me/summary"
        return await self.client.session.get(url, headers=self.HEADERS_SOCIAL)

    async def get_friends_summary_by_xuid(self, xuid):
        """
        Get friendlist summary of user by xuid

        Args:
            xuid (str): XUID to request summary from

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/xuid(%s)/summary" % xuid
        return await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
    
    async def get_friends_by_xuid(self, xuid):
        """
        Get friendlist of user by xuid

        Args:
            xuid (str): XUID to request summary from

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/xuid(%s)/people" % xuid
        return await self.client.session.get(url, headers=self.HEADERS_SOCIAL)

    async def get_friends_summary_by_gamertag(self, gamertag):
        """
        Get friendlist summary of user by xuid

        Args:
            gamertag (str): XUID to request friendlist from

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/gt(%s)/summary" % gamertag
        return await self.client.session.get(url, headers=self.HEADERS_SOCIAL)

    async def get_friends_own_batch(self, xuids):
        """
        Get friends metadata by providing a list of XUIDs

        Args:
            xuids (list): List of XUIDs

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if not isinstance(xuids, list):
            raise Exception("xuids parameter is not a list")

        url = self.SOCIAL_URL + "/users/me/people/xuids"
        post_data = {
            "xuids": [str(xuid) for xuid in xuids]
        }
        return await self.client.session.post(url, json=post_data, headers=self.HEADERS_SOCIAL)
