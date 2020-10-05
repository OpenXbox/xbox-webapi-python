"""
People - Access friendlist from own profiles and others
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.people.models import PeopleResponse, PeopleSummaryResponse


class PeopleProvider(BaseProvider):
    SOCIAL_URL = "https://social.xboxlive.com"
    HEADERS_SOCIAL = {"x-xbl-contract-version": "1"}

    async def get_friends_own(self) -> PeopleResponse:
        """
        Get friendlist of own profile

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/me/people"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())

    async def get_friends_summary_own(self) -> PeopleSummaryResponse:
        """
        Get friendlist summary of own profile

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/me/summary"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleSummaryResponse.parse_raw(await resp.text())

    async def get_friends_summary_by_xuid(self, xuid: str) -> PeopleSummaryResponse:
        """
        Get friendlist summary of user by xuid

        Args:
            xuid: XUID to request summary from

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + f"/users/xuid({xuid})/summary"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleSummaryResponse.parse_raw(await resp.text())

    async def get_friends_by_xuid(self, xuid: str) -> PeopleResponse:
        """
        Get friendlist of user by xuid

        Args:
            xuid: XUID to request summary from

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + f"/users/xuid({xuid})/people"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())

    async def get_friends_summary_by_gamertag(
        self, gamertag: str
    ) -> PeopleSummaryResponse:
        """
        Get friendlist summary of user by xuid

        Args:
            gamertag: XUID to request friendlist from

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + f"/users/gt({gamertag})/summary"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleSummaryResponse.parse_raw(await resp.text())

    async def get_friends_own_batch(self, xuids: List[str]) -> PeopleResponse:
        """
        Get friends metadata by providing a list of XUIDs

        Args:
            xuids: List of XUIDs

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.SOCIAL_URL + "/users/me/people/xuids"
        post_data = {"xuids": [str(xuid) for xuid in xuids]}
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_SOCIAL
        )
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())
