"""
Achievements

Get Xbox 360 and Xbox One Achievement data
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class AchievementsProvider(BaseProvider):
    ACHIEVEMENTS_URL = "https://achievements.xboxlive.com"
    HEADERS_GAME_360_PROGRESS = {'x-xbl-contract-version': '1'}
    HEADERS_GAME_PROGRESS = {'x-xbl-contract-version': '2'}

    def get_achievements_detail_item(self, xuid, service_config_id, achievement_id):
        """
        Get achievement detail for specific item

        Args:
            xuid (str): Xbox User Id
            service_config_id (str): Service Config Id
            achievement_id (str): Achievement Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.ACHIEVEMENTS_URL + "/users/xuid(%s)/achievements/%s/%s" % (xuid, service_config_id, achievement_id)
        return self.client.session.get(url, headers=self.HEADERS_GAME_PROGRESS)

    def get_achievements_xbox360_all(self, xuid, title_id):
        """
        Get all achievements for specific X360 title Id

        Args:
            xuid (str): Xbox User Id
            title_id (str): Xbox 360 Title Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.ACHIEVEMENTS_URL + "/users/xuid(%s)/titleachievements?" % xuid
        params = {
            "titleId": title_id
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAME_360_PROGRESS)

    def get_achievements_xbox360_earned(self, xuid, title_id):
        """
        Get earned achievements for specific X360 title id

        Args:
            xuid (str): Xbox User Id
            title_id (str): Xbox 360 Title Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.ACHIEVEMENTS_URL + "/users/xuid(%s)/achievements?" % xuid
        params = {
            "titleId": title_id
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAME_360_PROGRESS)

    def get_achievements_xbox360_recent_progress_and_info(self, xuid):
        """
        Get recent achievement progress and information

        Args:
            xuid (str): Xbox User Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.ACHIEVEMENTS_URL + "/users/xuid(%s)/history/titles" % xuid
        return self.client.session.get(url, headers=self.HEADERS_GAME_360_PROGRESS)

    def get_achievements_xboxone_gameprogress(self, xuid, title_id):
        """
        Get gameprogress for Xbox One title

        Args:
            xuid (str): Xbox User Id
            title_id (str): Xbox One Title Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.ACHIEVEMENTS_URL + "/users/xuid(%s)/achievements?" % xuid
        params = {
            "titleId": title_id
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAME_PROGRESS)

    def get_achievements_xboxone_recent_progress_and_info(self, xuid):
        """
        Get recent achievement progress and information

        Args:
            xuid (str): Xbox User Id

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.ACHIEVEMENTS_URL + "/users/xuid(%s)/history/titles" % xuid
        return self.client.session.get(url, headers=self.HEADERS_GAME_PROGRESS)
