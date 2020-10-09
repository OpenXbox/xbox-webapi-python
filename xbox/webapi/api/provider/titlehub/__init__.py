"""
Titlehub - Get Title history and info
"""
from typing import List, Optional

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.titlehub.models import TitleFields, TitleHubResponse


class TitlehubProvider(BaseProvider):
    TITLEHUB_URL = "https://titlehub.xboxlive.com"
    HEADERS_TITLEHUB = {
        "x-xbl-contract-version": "2",
        "x-xbl-client-name": "XboxApp",
        "x-xbl-client-type": "UWA",
        "x-xbl-client-version": "39.39.22001.0",
        "Accept-Language": "overwrite in __init__",
    }
    SEPARATOR = ","

    def __init__(self, client):
        """
        Initialize Baseclass, set 'Accept-Language' header from client instance

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super().__init__(client)
        self._headers = {**self.HEADERS_TITLEHUB}
        self._headers.update({"Accept-Language": self.client.language.locale})

    async def get_title_history(
        self,
        xuid: str,
        fields: Optional[List[TitleFields]] = None,
        max_items: Optional[int] = 5,
    ) -> TitleHubResponse:
        """
        Get recently played titles

        Args:
            xuid: Xuid
            fields: List of titlefield
            max_items: Maximum items

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT,
                TitleFields.IMAGE,
                TitleFields.SERVICE_CONFIG_ID,
            ]
        fields = self.SEPARATOR.join(fields)

        url = f"{self.TITLEHUB_URL}/users/xuid({xuid})/titles/titlehistory/decoration/{fields}"
        params = {"maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_TITLEHUB
        )
        resp.raise_for_status()
        return TitleHubResponse.parse_raw(await resp.text())

    async def get_title_info(
        self, title_id: str, fields: Optional[List[TitleFields]] = None
    ) -> TitleHubResponse:
        """
        Get info for specific title

        Args:
            title_id: Title Id
            fields: List of title fields

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT,
                TitleFields.ALTERNATE_TITLE_ID,
                TitleFields.DETAIL,
                TitleFields.IMAGE,
                TitleFields.SERVICE_CONFIG_ID,
            ]
        fields = self.SEPARATOR.join(fields)

        url = f"{self.TITLEHUB_URL}/users/xuid({self.client.xuid})/titles/titleid({title_id})/decoration/{fields}"
        resp = await self.client.session.get(url, headers=self.HEADERS_TITLEHUB)
        resp.raise_for_status()
        return TitleHubResponse.parse_raw(await resp.text())

    async def get_titles_batch(
        self, pfns: List[str], fields: Optional[List[TitleFields]] = None
    ) -> TitleHubResponse:
        """
        Get Title info via PFN ids

        Args:
            pfns: List of Package family names (e.g. 'Microsoft.XboxApp_8wekyb3d8bbwe')
            fields: List of title fields

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT,
                TitleFields.DETAIL,
                TitleFields.IMAGE,
                TitleFields.SERVICE_CONFIG_ID,
            ]
        fields = self.SEPARATOR.join(fields)

        url = self.TITLEHUB_URL + f"/titles/batch/decoration/{fields}"
        post_data = {"pfns": pfns, "windowsPhoneProductIds": []}
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_TITLEHUB
        )
        resp.raise_for_status()
        return TitleHubResponse.parse_raw(await resp.text())
