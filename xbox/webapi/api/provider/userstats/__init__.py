"""
Userstats - Get game statistics
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.userstats.models import GeneralStatsField


class UserStatsProvider(BaseProvider):
    USERSTATS_URL = "https://userstats.xboxlive.com"
    HEADERS_USERSTATS = {"x-xbl-contract-version": "2"}
    HEADERS_USERSTATS_WITH_METADATA = {"x-xbl-contract-version": "3"}
    SEPERATOR = ","

    async def get_stats(
        self, xuid: str, service_config_id: str, stats_fields: List = None
    ):
        """
        Get userstats

        Args:
            xuid: Xbox User Id
            service_config_id: Service Config Id of Game (scid)
            stats_fields: List of stats fields to acquire

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]
        stats = self.SEPERATOR.join(stats_fields)

        url = f"{self.USERSTATS_URL}/users/xuid({xuid})/scids/{service_config_id}/stats/{stats}"
        return await self.client.session.get(url, headers=self.HEADERS_USERSTATS)

    async def get_stats_with_metadata(
        self, xuid: str, service_config_id: str, stats_fields: List = None
    ):
        """
        Get userstats including metadata for each stat (if available)

        Args:
            xuid (str): Xbox User Id
            service_config_id (str): Service Config Id of Game (scid)
            stats_fields (list): List of stats fields to acquire

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]
        stats = self.SEPERATOR.join(stats_fields)

        url = f"{self.USERSTATS_URL}/users/xuid({xuid})/scids/{service_config_id}/stats/{stats}"
        params = {"include": "valuemetadata"}
        return await self.client.session.get(
            url, params=params, headers=self.HEADERS_USERSTATS_WITH_METADATA
        )

    async def get_stats_batch(
        self, xuids: List, title_id: int, stats_fields: List = None
    ):
        """
        Get userstats in batch mode

        Args:
            xuids (list): List of XUIDs to get stats for
            title_id (int): Game Title Id
            stats_fields (list): List of stats fields to acquire

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if not isinstance(xuids, list):
            raise ValueError("Xuids parameter is not a list")

        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]

        url = self.USERSTATS_URL + "/batch"
        post_data = {
            "arrangebyfield": "xuid",
            "groups": [{"name": "Hero", "titleId": int(title_id)}],
            "stats": [dict(name=stat, titleId=int(title_id)) for stat in stats_fields],
            "xuids": [str(xid) for xid in xuids],
        }
        return await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_USERSTATS
        )

    async def get_stats_batch_by_scid(
        self, xuids: List, service_config_id: str, stats_fields: List = None
    ):
        """
        Get userstats in batch mode, via scid

        Args:
            xuids: List of XUIDs to get stats for
            service_config_id: Service Config Id of Game (scid)
            stats_fields: List of stats fields to acquire

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if not isinstance(xuids, list):
            raise ValueError("Xuids parameter is not a list")

        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]

        url = self.USERSTATS_URL + "/batch"

        post_data = {
            "arrangebyfield": "xuid",
            "groups": [{"name": "Hero", "scid": service_config_id}],
            "stats": [dict(name=stat, scid=service_config_id) for stat in stats_fields],
            "xuids": [str(xid) for xid in xuids],
        }
        return await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_USERSTATS
        )
