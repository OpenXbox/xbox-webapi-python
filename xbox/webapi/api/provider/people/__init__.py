"""
People - Access friendlist from own profiles and others
"""

from xbox.webapi.api.provider.people.models import (
    PeopleDecoration,
    PeopleResponse,
    PeopleSummaryResponse,
)
from xbox.webapi.api.provider.ratelimitedprovider import RateLimitedProvider
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xbox.webapi.api.client import XboxLiveClient

class PeopleProvider(RateLimitedProvider):
    SOCIAL_URL = "https://social.xboxlive.com"
    HEADERS_SOCIAL = {"x-xbl-contract-version": "2"}
    PEOPLE_URL = "https://peoplehub.xboxlive.com"
    HEADERS_PEOPLE = {
        "x-xbl-contract-version": "7",
        "Accept-Language": "overwrite in __init__",
    }
    SEPERATOR = ","

    # NOTE: Rate Limits are noted for social.xboxlive.com ONLY
    RATE_LIMITS = {"burst": 10, "sustain": 30}

    client: "XboxLiveClient"

    def __init__(self, client: "XboxLiveClient") -> None:
        """
        Initialize Baseclass, set 'Accept-Language' header from client instance

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super().__init__(client)
        self._headers = {**self.HEADERS_PEOPLE}
        self._headers.update({"Accept-Language": self.client.language.locale})

    async def get_friends_own(
        self, decoration_fields: list[PeopleDecoration] | None = None, **kwargs
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

        url = f"{self.PEOPLE_URL}/users/me/people/friends/decoration/{decoration}"
        resp = await self.client.session.get(url, headers=self._headers, **kwargs)
        resp.raise_for_status()
        return PeopleResponse(**resp.json())

    async def get_friends_by_xuid(
        self, xuid: str, decoration_fields: list[PeopleDecoration] | None = None, **kwargs
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

        url = f"{self.PEOPLE_URL}/users/me/people/xuids({xuid})/decoration/{decoration}"
        resp = await self.client.session.get(url, headers=self._headers, **kwargs)
        resp.raise_for_status()
        return PeopleResponse(**resp.json())

    async def get_friends_own_batch(
        self,
        xuids: list[str],
        decoration_fields: list[PeopleDecoration] | None = None,
        **kwargs,
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
            url, json={"xuids": xuids}, headers=self._headers, **kwargs
        )
        resp.raise_for_status()
        return PeopleResponse(**resp.json())

    async def get_friend_recommendations(self, decoration_fields: list[PeopleDecoration] | None = None, **kwargs) -> PeopleResponse:
        """
        Get recommended friends

        Returns:
            :class:`PeopleResponse`: People Response
        """
        if not decoration_fields:
            decoration_fields = [PeopleDecoration.DETAIL]
        decoration = self.SEPERATOR.join(decoration_fields)

        url = f"{self.PEOPLE_URL}/users/me/people/recommendations/decoration/{decoration}"
        resp = await self.client.session.get(url, headers=self._headers, **kwargs)
        resp.raise_for_status()
        return PeopleResponse(**resp.json())

    async def get_friends_summary_own(self, **kwargs) -> PeopleSummaryResponse:
        """
        Get friendlist summary of own profile

        Returns:
            :class:`PeopleSummaryResponse`: People Summary Response
        """
        url = self.SOCIAL_URL + "/users/me/summary"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_SOCIAL, rate_limits=self.rate_limit_read, **kwargs
        )
        resp.raise_for_status()
        return PeopleSummaryResponse(**resp.json())

    async def get_friends_summary_by_xuid(
        self, xuid: str, **kwargs
    ) -> PeopleSummaryResponse:
        """
        Get friendlist summary of user by xuid

        Args:
            xuid: XUID to request summary from

        Returns:
            :class:`PeopleSummaryResponse`: People Summary Response
        """
        url = self.SOCIAL_URL + f"/users/xuid({xuid})/summary"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_SOCIAL, rate_limits=self.rate_limit_read, **kwargs
        )
        resp.raise_for_status()
        return PeopleSummaryResponse(**resp.json())

    async def get_friends_summary_by_gamertag(
        self, gamertag: str, **kwargs
    ) -> PeopleSummaryResponse:
        """
        Get friendlist summary of user by gamertag

        Args:
            gamertag: Gamertag to request friendlist from

        Returns:
            :class:`PeopleSummaryResponse`: People Summary Response
        """
        url = self.SOCIAL_URL + f"/users/gt({gamertag})/summary"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_SOCIAL, rate_limits=self.rate_limit_read, **kwargs
        )
        resp.raise_for_status()
        return PeopleSummaryResponse(**resp.json())
