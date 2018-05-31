"""
Titlehub - Get Title history and info
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class TitleFields(object):
    ACHIEVEMENT = "achievement"
    IMAGE = "image"
    FRIENDS_WHO_PLAYED = "friendswhoplayed"
    SERVICE_CONFIG_ID = "SCID"
    DETAIL = "detail"
    ALTERNATE_TITLE_ID = "alternateTitleId"


class TitlehubProvider(BaseProvider):
    TITLEHUB_URL = "https://titlehub.xboxlive.com"
    HEADERS_TITLEHUB = {
        'x-xbl-contract-version': '2',
        'x-xbl-client-name': 'XboxApp',
        'x-xbl-client-type': 'UWA',
        'x-xbl-client-version': '39.39.22001.0',
        'Accept-Language': 'overwrite in __init__'
    }
    SEPARATOR = ","

    def __init__(self, client):
        """
        Initialize Baseclass, set 'Accept-Language' header from client instance

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super(TitlehubProvider, self).__init__(client)
        self.HEADERS_TITLEHUB.update({'Accept-Language': self.client.language.locale})

    def get_title_history(self, xuid, fields=None, max_items=5):
        """
        Get recently played titles

        Args:
            xuid (int/str): Xuid
            fields (list): Members of :class:`TitleFields`
            max_items (int): Maximum items

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not fields:
            fields = [TitleFields.ACHIEVEMENT, TitleFields.IMAGE, TitleFields.SERVICE_CONFIG_ID]
        fields = self.SEPARATOR.join(fields)

        url = self.TITLEHUB_URL + "/users/xuid(%s)/titles/titlehistory/decoration/%s" % (xuid, fields)
        params = {
            'maxItems': max_items
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_TITLEHUB)

    def get_title_info(self, title_id, fields=None):
        """
        Get info for specific title

        Args:
            title_id (str): Title Id
            fields (list): Members of :class:`TitleFields`

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT, TitleFields.ALTERNATE_TITLE_ID, TitleFields.DETAIL,
                TitleFields.IMAGE, TitleFields.SERVICE_CONFIG_ID
            ]
        fields = self.SEPARATOR.join(fields)

        url = self.TITLEHUB_URL + "/users/xuid(%s)/titles/titleid(%s)/decoration/%s" % (self.client.xuid, title_id, fields)
        return self.client.session.get(url, headers=self.HEADERS_TITLEHUB)

    def get_titles_batch(self, pfns, fields=None):
        """
        Get Title info via PFN ids

        Args:
            pfns (list): PFN Id strings (e.g. 'Microsoft.XboxApp_8wekyb3d8bbwe')
            fields (list): Members of :class:`TitleFields`

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        if not isinstance(pfns, list):
            raise ValueError("PFN parameter requires list of strings")

        if not fields:
            fields = [TitleFields.ACHIEVEMENT, TitleFields.DETAIL, TitleFields.IMAGE, TitleFields.SERVICE_CONFIG_ID]
        fields = self.SEPARATOR.join(fields)

        url = self.TITLEHUB_URL + "/titles/batch/decoration/%s" % fields
        post_data = {
            "pfns": pfns,
            "windowsPhoneProductIds": []
        }
        return self.client.session.post(url, json=post_data, headers=self.HEADERS_TITLEHUB)
