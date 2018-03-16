"""
EPLists - Mainly used for XBL Pins
"""


class ListsProvider(object):
    LISTS_URL = "https://eplists.xboxlive.com"
    HEADERS_LISTS = {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Pragma': 'no-cache',
        'x-xbl-client-type': 'Companion',
        'x-xbl-client-version': '2.0',
        'x-xbl-contract-version': '3.2',
        'x-xbl-device-type': 'WindowsPhone',
        'x-xbl-isautomated-client': 'true'
    }

    SEPERATOR = "."

    def __init__(self, client):
        """
        Initialize an instance of GamerpicsProvider

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        self.client = client

    def remove_items(self, xuid, params, listname="XBLPins"):
        """
        Remove items from specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.LISTS_URL + "/users/xuid(%s)/lists/PINS/%s" % (xuid, listname)
        return self.client.session.delete(url, params=params, headers=self.HEADERS_LISTS)

    def get_items(self, xuid, params, listname="XBLPins"):
        """
        Get items from specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.LISTS_URL + "/users/xuid(%s)/lists/PINS/%s" % (xuid, listname)
        return self.client.session.get(url, params=params, headers=self.HEADERS_LISTS)

    def insert_items(self, xuid, params, listname="XBLPins"):
        """
        Insert items to specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.LISTS_URL + "/users/xuid(%s)/lists/PINS/%s" % (xuid, listname)
        return self.client.session.post(url, params=params, headers=self.HEADERS_LISTS)

    def update_items(self, xuid, params, listname="XBLPins"):
        """
        Update items in specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.LISTS_URL + "/users/xuid(%s)/lists/PINS/%s" % (xuid, listname)
        return self.client.session.put(url, params=params, headers=self.HEADERS_LISTS)
