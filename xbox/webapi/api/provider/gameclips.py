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

    def get_recent_own_clips(self, title_id=None, skip_items=0, max_items=25):
        """
        Get own recent clips, optionally filter for title Id

        Args:
            title_id (int): Title ID to filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/me"
        if title_id:
            url += "/titles/%s" % title_id
        url += "/clips"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)

    def get_recent_clips_by_xuid(self, xuid, title_id=None, skip_items=0, max_items=25):
        """
        Get clips by XUID, optionally filter for title Id

        Args:
            xuid (str): XUID of user to get clips from
            title_id (str): Optional title id filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/xuid(%s)" % xuid
        if title_id:
            url += "/titles/%s" % title_id
        url += "/clips"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)

    def get_saved_community_clips_by_title_id(self, title_id):
        """
        Get saved community clips by Title Id

        Args:
            title_id (str): Title Id to get screenshots for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/public/titles/%s/clips/saved" % title_id
        params = {
            "qualifier": "created"
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)

    def get_saved_own_clips(self, title_id=None, skip_items=0, max_items=25):
        """
        Get own saved clips, optionally filter for title Id an

        Args:
            title_id (int): Optional Title ID to filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/me"
        if title_id:
            url += "/titles/%s" % title_id
        url += "/clips/saved"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)

    def get_saved_clips_by_xuid(self, xuid, title_id=None, skip_items=0, max_items=25):
        """
        Get saved clips by XUID, optionally filter for title Id

        Args:
            xuid (str): XUID of user to get screenshots from
            title_id (str): Optional title id filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMECLIPS_METADATA_URL + "/users/xuid(%s)" % xuid
        if title_id:
            url += "/titles/%s" % title_id
        url += "/clips/saved"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_GAMECLIPS_METADATA)
