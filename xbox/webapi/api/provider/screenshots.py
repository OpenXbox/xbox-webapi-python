"""
Screenshots - Get screenshot info
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class ScreenshotsProvider(BaseProvider):
    SCREENSHOTS_METADATA_URL = "https://screenshotsmetadata.xboxlive.com"
    HEADERS_SCREENSHOTS_METADATA = {'x-xbl-contract-version': '5'}

    def get_recent_community_screenshots_by_title_id(self, title_id):
        """
        Get recent community screenshots by Title Id

        Args:
            title_id (str): Title Id to get screenshots for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/public/titles/%s/screenshots" % title_id
        params = {
            "qualifier": "created"
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA)

    def get_recent_own_screenshots(self, title_id=None, skip_items=0, max_items=25):
        """
        Get own recent screenshots, optionally filter for title Id

        Args:
            title_id (int): Title ID to filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/users/me"
        if title_id:
            url += "/titles/%s" % title_id
        url += "/screenshots"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA)

    def get_recent_screenshots_by_xuid(self, xuid, title_id=None, skip_items=0, max_items=25):
        """
        Get recent screenshots by XUID, optionally filter for title Id

        Args:
            xuid (str): XUID of user to get screenshots from
            title_id (str): Optional title id filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/users/xuid(%s)" % xuid
        if title_id:
            url += "/titles/%s" % title_id
        url += "/screenshots"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA)

    def get_saved_community_screenshots_by_title_id(self, title_id):
        """
        Get saved community screenshots by Title Id

        Args:
            title_id (str): Title Id to get screenshots for

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/public/titles/%s/screenshots/saved" % title_id
        params = {
            "qualifier": "created"
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA)

    def get_saved_own_screenshots(self, title_id=None, skip_items=0, max_items=25):
        """
        Get own saved screenshots, optionally filter for title Id an

        Args:
            title_id (int): Optional Title ID to filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/users/me"
        if title_id:
            url += "/titles/%s" % title_id
        url += "/screenshots/saved"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA)

    def get_saved_screenshots_by_xuid(self, xuid, title_id=None, skip_items=0, max_items=25):
        """
        Get saved screenshots by XUID, optionally filter for title Id

        Args:
            xuid (str): XUID of user to get screenshots from
            title_id (str): Optional title id filter
            skip_items (int): Item count to skip
            max_items (int): Maximum item count to load

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.SCREENSHOTS_METADATA_URL + "/users/xuid(%s)" % xuid
        if title_id:
            url += "/titles/%s" % title_id
        url += "/screenshots/saved"

        params = {
            'skipItems': skip_items,
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_SCREENSHOTS_METADATA)
