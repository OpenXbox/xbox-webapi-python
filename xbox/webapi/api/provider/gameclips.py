"""
Gameclips - Get gameclip info
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class GameclipProvider(BaseProvider):
    GAMECLIPS_METADATA_URL = "https://gameclipsmetadata.xboxlive.com"
    HEADERS_GAMECLIPS_METADATA = {'x-xbl-contract-version': '1'}

    def get_recent_community_clips_by_title_id(self, title_id):
        """
        Get recent community clips by Title Id

        Args:
            title_id (str): Title Id to get clips for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/public/titles/%s/clips?" % title_id
        params = {
            "qualifier": "created"
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)

    def get_recent_own_clips(self, skip_items=0, max_items=25):
        """
        Get own recent clips

        Args:
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/me/clips"
        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)

    def get_recent_clips_by_xuid(self, xuid, skip_items=0, max_items=25):
        """
        Get clips by XUID

        Args:
            xuid (str): XUID of user to get clips from
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/xuid(%s)/clips" % xuid
        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)
