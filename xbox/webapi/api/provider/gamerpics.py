"""
Gamerpics

Upload and download your gamerpicture
"""


class GamerpicsProvider(object):
    GAMERPICS_URL = "https://gamerpics.xboxlive.com"
    HEADERS_GAMERPICS = {
        'x-xbl-client-type': 'Durango',
        'x-xbl-client-version': '0',
        'x-xbl-contract-version': '1',
        'x-xbl-device-type': 'Console'
    }

    def __init__(self, client):
        """
        Initialize an instance of GamerpicsProvider

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        self.client = client

    def download_gamerpic(self):
        """
        Download your own gamerpicture

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMERPICS_URL + "/users/me/gamerpic"
        return self.client.session.get(url, headers=self.HEADERS_GAMERPICS)

    def upload_gamerpic(self, png_data):
        """
        Upload a new gamerpicture for your profile

        Args:
            png_data (bytes): New image

        Returns:
            :class:`requests.Response`: HTTP Response
        """
        url = self.GAMERPICS_URL + "/users/me/gamerpic"
        return self.client.session.post(url, data=png_data, headers=self.HEADERS_GAMERPICS)
