"""
Userstats - Get game statistics
"""
from typing import List, Optional

from xbox.webapi.api.provider.ratelimitedprovider import RateLimitedProvider
from xbox.webapi.api.provider.userstats.models import (
    GeneralStatsField,
    UserStatsResponse,
)


class UserStatsProvider(RateLimitedProvider):
    USERSTATS_URL = "https://userstats.xboxlive.com"
    HEADERS_USERSTATS = {"x-xbl-contract-version": "2"}
    HEADERS_USERSTATS_WITH_METADATA = {"x-xbl-contract-version": "3"}
    SEPERATOR = ","

    # NOTE: Stats Read (userstats.xboxlive.com) and Stats Write (statswrite.xboxlive.com)
    # Are mentioned as their own objects but their rate limits are the same and do not collide
    # (Stats Read -> read rate limit, Stats Write -> write rate limit)
    RATE_LIMITS = {"burst": 100, "sustain": 300}

    async def get_stats(
        self,
        xuid: str,
        service_config_id: str,
        stats_fields: Optional[List[GeneralStatsField]] = None,
        **kwargs,
    ) -> UserStatsResponse:
        """
        Get userstats

        Args:
            xuid: Xbox User Id
            service_config_id: Service Config Id of Game (scid)
            stats_fields: List of stats fields to acquire

        Returns:
            :class:`UserStatsResponse`: User Stats Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]
        stats = self.SEPERATOR.join(stats_fields)

        url = f"{self.USERSTATS_URL}/users/xuid({xuid})/scids/{service_config_id}/stats/{stats}"
        resp = await self.client.session.get(
            url,
            headers=self.HEADERS_USERSTATS,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return UserStatsResponse(**resp.json())

    async def get_stats_with_metadata(
        self,
        xuid: str,
        service_config_id: str,
        stats_fields: Optional[List[GeneralStatsField]] = None,
        **kwargs,
    ) -> UserStatsResponse:
        """
        Get userstats including metadata for each stat (if available)

        Args:
            xuid: Xbox User Id
            service_config_id: Service Config Id of Game (scid)
            stats_fields: List of stats fields to acquire

        Returns:
            :class:`UserStatsResponse`: User Stats Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]
        stats = self.SEPERATOR.join(stats_fields)

        url = f"{self.USERSTATS_URL}/users/xuid({xuid})/scids/{service_config_id}/stats/{stats}"
        params = {"include": "valuemetadata"}
        resp = await self.client.session.get(
            url,
            params=params,
            headers=self.HEADERS_USERSTATS_WITH_METADATA,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return UserStatsResponse(**resp.json())

    async def get_stats_batch(
        self,
        xuids: List[str],
        title_id: str,
        stats_fields: Optional[List[GeneralStatsField]] = None,
        **kwargs,
    ) -> UserStatsResponse:
        """
        Get userstats in batch mode

        Args:
            xuids: List of XUIDs to get stats for
            title_id: Game Title Id
            stats_fields: List of stats fields to acquire

        Returns:
            :class:`UserStatsResponse`: User Stats Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]

        url = self.USERSTATS_URL + "/batch"
        post_data = {
            "arrangebyfield": "xuid",
            "groups": [{"name": "Hero", "titleId": title_id}],
            "stats": [dict(name=stat, titleId=title_id) for stat in stats_fields],
            "xuids": xuids,
        }
        resp = await self.client.session.post(
            url,
            json=post_data,
            headers=self.HEADERS_USERSTATS,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return UserStatsResponse(**resp.json())

    async def get_stats_batch_by_scid(
        self,
        xuids: List[str],
        service_config_id: str,
        stats_fields: Optional[List[GeneralStatsField]] = None,
        **kwargs,
    ) -> UserStatsResponse:
        """
        Get userstats in batch mode, via scid

        Args:
            xuids: List of XUIDs to get stats for
            service_config_id: Service Config Id of Game (scid)
            stats_fields: List of stats fields to acquire

        Returns:
            :class:`UserStatsResponse`: User Stats Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]

        url = self.USERSTATS_URL + "/batch"

        post_data = {
            "arrangebyfield": "xuid",
            "groups": [{"name": "Hero", "scid": service_config_id}],
            "stats": [dict(name=stat, scid=service_config_id) for stat in stats_fields],
            "xuids": xuids,
        }
        resp = await self.client.session.post(
            url,
            json=post_data,
            headers=self.HEADERS_USERSTATS,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return UserStatsResponse(**resp.json())
