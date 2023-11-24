"""
Presence - Get online status of friends
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.presence.models import (
    PresenceBatchResponse,
    PresenceItem,
    PresenceLevel,
    PresenceState,
)


class PresenceProvider(BaseProvider):
    PRESENCE_URL = "https://userpresence.xboxlive.com"
    HEADERS_PRESENCE = {"x-xbl-contract-version": "3", "Accept": "application/json"}

    async def get_presence(
        self,
        xuid,
        presence_level: PresenceLevel = PresenceLevel.USER,
        **kwargs,
    ) -> PresenceItem:
        """
        Get presence for given xuid

        Args:
            xuid: XUID
            presence_level: Filter level

        Returns:
            :class:`PresenceItem`: Presence Response
        """
        url = self.PRESENCE_URL + "/users/xuid(" + xuid + ")?level=" + presence_level

        resp = await self.client.session.get(
            url, headers=self.HEADERS_PRESENCE, **kwargs
        )
        resp.raise_for_status()
        return PresenceItem(**resp.json())

    async def get_presence_batch(
        self,
        xuids: List[str],
        online_only: bool = False,
        presence_level: PresenceLevel = PresenceLevel.USER,
        **kwargs,
    ) -> List[PresenceItem]:
        """
        Get presence for list of xuids

        Args:
            xuids: List of XUIDs
            online_only: Only get online profiles
            presence_level: Filter level

        Returns: List[:class:`PresenceItem`]: List of presence items
        """
        if len(xuids) > 1100:
            raise Exception("Xuid list length is > 1100")

        url = self.PRESENCE_URL + "/users/batch"
        post_data = {
            "users": [str(x) for x in xuids],
            "onlineOnly": online_only,
            "level": presence_level,
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_PRESENCE, **kwargs
        )
        resp.raise_for_status()
        parsed = PresenceBatchResponse.model_validate(resp.json())
        return parsed.root

    async def get_presence_own(
        self, presence_level: PresenceLevel = PresenceLevel.ALL, **kwargs
    ) -> PresenceItem:
        """
        Get presence of own profile

        Args:
            presence_level: Filter level

        Returns:
            :class:`PresenceItem`: Presence Response
        """
        url = self.PRESENCE_URL + "/users/me"
        params = {"level": presence_level}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_PRESENCE, **kwargs
        )
        resp.raise_for_status()
        return PresenceItem(**resp.json())

    async def set_presence_own(self, presence_state: PresenceState, **kwargs) -> bool:
        """
        Set presence of own profile

        Args:
            presence_state: State of presence

        Returns:
            `True` on success, `False` otherwise
        """
        url = self.PRESENCE_URL + f"/users/xuid({self.client.xuid})/state"
        data = {"state": presence_state.value}
        resp = await self.client.session.put(
            url, json=data, headers=self.HEADERS_PRESENCE, **kwargs
        )
        return resp.status_code == 200
