"""
Achievements

Get Xbox 360 and Xbox One Achievement data
"""
from xbox.webapi.api.provider.achievements.models import (
    Achievement360ProgressResponse,
    Achievement360Response,
    AchievementResponse,
    RecentProgressResponse,
)
from xbox.webapi.api.provider.baseprovider import BaseProvider


class AchievementsProvider(BaseProvider):
    ACHIEVEMENTS_URL = "https://achievements.xboxlive.com"
    HEADERS_GAME_360_PROGRESS = {"x-xbl-contract-version": "1"}
    HEADERS_GAME_PROGRESS = {"x-xbl-contract-version": "2"}

    async def get_achievements_detail_item(
        self, xuid, service_config_id, achievement_id
    ) -> AchievementResponse:
        """
        Get achievement detail for specific item

        Args:
            xuid (str): Xbox User Id
            service_config_id (str): Service Config Id
            achievement_id (str): Achievement Id

        Returns:
            :class:`AchievementResponse`: Achievement Response
        """
        url = f"{self.ACHIEVEMENTS_URL}/users/xuid({xuid})/achievements/{service_config_id}/{achievement_id}"
        resp = await self.client.session.get(url, headers=self.HEADERS_GAME_PROGRESS)
        resp.raise_for_status()
        return AchievementResponse.parse_raw(await resp.text())

    async def get_achievements_xbox360_all(
        self, xuid, title_id
    ) -> Achievement360Response:
        """
        Get all achievements for specific X360 title Id

        Args:
            xuid (str): Xbox User Id
            title_id (str): Xbox 360 Title Id

        Returns:
            :class:`Achievement360Response`: Achievement 360 Response
        """
        url = f"{self.ACHIEVEMENTS_URL}/users/xuid({xuid})/titleachievements?"
        params = {"titleId": title_id}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAME_360_PROGRESS
        )
        resp.raise_for_status()
        return Achievement360Response.parse_raw(await resp.text())

    async def get_achievements_xbox360_earned(
        self, xuid, title_id
    ) -> Achievement360Response:
        """
        Get earned achievements for specific X360 title id

        Args:
            xuid (str): Xbox User Id
            title_id (str): Xbox 360 Title Id

        Returns:
            :class:`Achievement360Response`: Achievement 360 Response
        """
        url = f"{self.ACHIEVEMENTS_URL}/users/xuid({xuid})/achievements?"
        params = {"titleId": title_id}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAME_360_PROGRESS
        )
        resp.raise_for_status()
        return Achievement360Response.parse_raw(await resp.text())

    async def get_achievements_xbox360_recent_progress_and_info(
        self, xuid
    ) -> Achievement360ProgressResponse:
        """
        Get recent achievement progress and information

        Args:
            xuid (str): Xbox User Id

        Returns:
            :class:`Achievement360Response`: Achievement 360 Response
        """
        url = f"{self.ACHIEVEMENTS_URL}/users/xuid({xuid})/history/titles"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_GAME_360_PROGRESS
        )
        resp.raise_for_status()
        return Achievement360ProgressResponse.parse_raw(await resp.text())

    async def get_achievements_xboxone_gameprogress(
        self, xuid, title_id
    ) -> AchievementResponse:
        """
        Get gameprogress for Xbox One title

        Args:
            xuid (str): Xbox User Id
            title_id (str): Xbox One Title Id

        Returns:
            :class:`AchievementResponse`: Achievement Response
        """
        url = f"{self.ACHIEVEMENTS_URL}/users/xuid({xuid})/achievements?"
        params = {"titleId": title_id}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_GAME_PROGRESS
        )
        resp.raise_for_status()
        return AchievementResponse.parse_raw(await resp.text())

    async def get_achievements_xboxone_recent_progress_and_info(
        self, xuid
    ) -> RecentProgressResponse:
        """
        Get recent achievement progress and information

        Args:
            xuid (str): Xbox User Id

        Returns:
            :class:`RecentProgressResponse`: Recent Progress Response
        """
        url = f"{self.ACHIEVEMENTS_URL}/users/xuid({xuid})/history/titles"
        resp = await self.client.session.get(url, headers=self.HEADERS_GAME_PROGRESS)
        resp.raise_for_status()
        return RecentProgressResponse.parse_raw(await resp.text())
