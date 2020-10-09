"""
People - Access friendlist from own profiles and others
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.people.models import (
    PeopleDecoration,
    PeopleResponse,
    PeopleSummaryResponse,
)


class PeopleProvider(BaseProvider):
    SOCIAL_URL = "https://social.xboxlive.com"
    HEADERS_SOCIAL = {"x-xbl-contract-version": "2"}
    PEOPLE_URL = "https://peoplehub.xboxlive.com"
    HEADERS_PEOPLE = {
        "x-xbl-contract-version": "3",
        "Accept-Language": "overwrite in __init__",
    }
    SEPERATOR = ","

    def __init__(self, client):
        """
        Initialize Baseclass, set 'Accept-Language' header from client instance

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super().__init__(client)
        self._headers = {**self.HEADERS_PEOPLE}
        self._headers.update({"Accept-Language": self.client.language.locale})

    async def get_friends_own(
        self, decoration_fields: List[PeopleDecoration] = None
    ) -> PeopleResponse:
        """
        Get friendlist of own profile

        Returns:
            :class:`PeopleResponse`: People Response
        """
        if not decoration_fields:
            decoration_fields = [
                PeopleDecoration.PREFERRED_COLOR,
                PeopleDecoration.DETAIL,
                PeopleDecoration.MULTIPLAYER_SUMMARY,
                PeopleDecoration.PRESENCE_DETAIL,
            ]
        decoration = self.SEPERATOR.join(decoration_fields)

        url = f"{self.PEOPLE_URL}/users/me/people/social/decoration/{decoration}"
        resp = await self.client.session.get(url, headers=self._headers)
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())

    async def get_friends_by_xuid(
        self, xuid: str, decoration_fields: List[PeopleDecoration] = None
    ) -> PeopleResponse:
        """
        Get friendlist of own profile

        Returns:
            :class:`PeopleResponse`: People Response
        """
        if not decoration_fields:
            decoration_fields = [
                PeopleDecoration.PREFERRED_COLOR,
                PeopleDecoration.DETAIL,
                PeopleDecoration.MULTIPLAYER_SUMMARY,
                PeopleDecoration.PRESENCE_DETAIL,
            ]
        decoration = self.SEPERATOR.join(decoration_fields)

        url = f"{self.PEOPLE_URL}/users/xuid({xuid})/people/social/decoration/{decoration}"
        resp = await self.client.session.get(url, headers=self._headers)
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())

    async def get_friends_own_batch(
        self, xuids: List[str], decoration_fields: List[PeopleDecoration] = None
    ) -> PeopleResponse:
        """
        Get friends metadata by providing a list of XUIDs

        Args:
            xuids: List of XUIDs

        Returns:
            :class:`PeopleResponse`: People Response
        """
        if not decoration_fields:
            decoration_fields = [
                PeopleDecoration.PREFERRED_COLOR,
                PeopleDecoration.DETAIL,
                PeopleDecoration.MULTIPLAYER_SUMMARY,
                PeopleDecoration.PRESENCE_DETAIL,
            ]
        decoration = self.SEPERATOR.join(decoration_fields)

        url = f"{self.PEOPLE_URL}/users/me/people/batch/decoration/{decoration}"
        resp = await self.client.session.post(
            url, json={"xuids": xuids}, headers=self._headers
        )
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())

    async def get_friend_recommendations(self) -> PeopleResponse:
        """
        Get recommended friends

        Returns:
            :class:`PeopleResponse`: People Response
        """
        url = f"{self.PEOPLE_URL}/users/me/people/recommendations"
        resp = await self.client.session.get(url, headers=self._headers)
        resp.raise_for_status()
        return PeopleResponse.parse_raw(await resp.text())

    async def get_friends_summary_own(self) -> PeopleSummaryResponse:
        """
        Get friendlist summary of own profile

        Returns:
            :class:`PeopleSummaryResponse`: People Summary Response
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
            :class:`PeopleSummaryResponse`: People Summary Response
        """
        url = self.SOCIAL_URL + f"/users/xuid({xuid})/summary"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleSummaryResponse.parse_raw(await resp.text())

    async def get_friends_summary_by_gamertag(
        self, gamertag: str
    ) -> PeopleSummaryResponse:
        """
        Get friendlist summary of user by gamertag

        Args:
            gamertag: Gamertag to request friendlist from

        Returns:
            :class:`PeopleSummaryResponse`: People Summary Response
        """
        url = self.SOCIAL_URL + f"/users/gt({gamertag})/summary"
        resp = await self.client.session.get(url, headers=self.HEADERS_SOCIAL)
        resp.raise_for_status()
        return PeopleSummaryResponse.parse_raw(await resp.text())
