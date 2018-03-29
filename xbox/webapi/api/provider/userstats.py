"""
Userstats - Get game statistics
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class UserStatsProvider(BaseProvider):
    USERSTATS_URL = "https://userstats.xboxlive.com"
    HEADERS_USERSTATS = {'x-xbl-contract-version': '2'}
    HEADERS_USERSTATS_WITH_METADATA = {'x-xbl-contract-version': '3'}
    SEPERATOR = ","

    def get_stats(self, xuid, service_config_id, stats_fields=None):
        """
        Get userstats

        Args:
            xuid (str): Xbox User Id
            service_config_id (str): Service Config Id of Game (scid)
            stats_fields (list): List of stats fields to acquire

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]
        stats = self.SEPERATOR.join(stats_fields)

        url = self.USERSTATS_URL + "/users/xuid(%s)/scids/%s/stats/%s" % (xuid, service_config_id, stats)
        return self.client.session.get(url, headers=self.HEADERS_USERSTATS)

    def get_stats_with_metadata(self, xuid, service_config_id, stats_fields=None):
        """
        Get userstats including metadata for each stat (if available)

        Args:
            xuid (str): Xbox User Id
            service_config_id (str): Service Config Id of Game (scid)
            stats_fields (list): List of stats fields to acquire

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]
        stats = self.SEPERATOR.join(stats_fields)

        url = self.USERSTATS_URL + "/users/xuid(%s)/scids/%s/stats/%s" % (xuid, service_config_id, stats)
        params = {
            'include': 'valuemetadata'
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_USERSTATS_WITH_METADATA)

    def get_stats_batch(self, xuids, title_id, stats_fields=None):
        """
        Get userstats in batch mode

        Args:
            xuids (list): List of XUIDs to get stats for
            title_id (int): Game Title Id
            stats_fields (list): List of stats fields to acquire

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(xuids, list):
            raise ValueError('Xuids parameter is not a list')

        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]

        url = self.USERSTATS_URL + "/batch"
        post_data = {
            'arrangebyfield': 'xuid',
            'groups': [
                {
                    'name': 'Hero',
                    'titleId': int(title_id)
                }
            ],
            'stats': [dict(name=stat, titleId=int(title_id)) for stat in stats_fields],
            'xuids': [str(xid) for xid in xuids]
        }
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_USERSTATS)

    def get_stats_batch_by_scid(self, xuids, service_config_id, stats_fields=None):
        """
        Get userstats in batch mode, via scid

        Args:
            xuids (list): List of XUIDs to get stats for
            service_config_id (int): Service Config Id of Game (scid)
            stats_fields (list): List of stats fields to acquire

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(xuids, list):
            raise ValueError('Xuids parameter is not a list')

        if not stats_fields:
            stats_fields = [GeneralStatsField.MINUTES_PLAYED]

        url = self.USERSTATS_URL + "/batch"

        post_data = {
            'arrangebyfield': 'xuid',
            'groups': [
                {
                    'name': 'Hero',
                    'scid': service_config_id
                }
            ],
            'stats': [dict(name=stat, scid=service_config_id) for stat in stats_fields],
            'xuids': [str(xid) for xid in xuids]
        }
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_USERSTATS)


class GeneralStatsField(object):
    MINUTES_PLAYED = "MinutesPlayed"
