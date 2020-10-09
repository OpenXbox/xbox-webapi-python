"""
EPLists - Mainly used for XBL Pins
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.lists.models import ListMetadata, ListsResponse


class ListsProvider(BaseProvider):
    LISTS_URL = "https://eplists.xboxlive.com"
    HEADERS_LISTS = {"Content-Type": "application/json", "x-xbl-contract-version": "2"}

    SEPERATOR = "."

    async def remove_items(
        self, xuid: str, post_body: dict, listname: str = "XBLPins"
    ) -> ListMetadata:
        """
        Remove items from specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`ListMetadata`: List Metadata Response
        """
        url = self.LISTS_URL + f"/users/xuid({xuid})/lists/PINS/{listname}"
        resp = await self.client.session.delete(
            url, json=post_body, headers=self.HEADERS_LISTS
        )
        resp.raise_for_status()
        return ListMetadata.parse_raw(await resp.text())

    async def get_items(self, xuid: str, listname: str = "XBLPins") -> ListsResponse:
        """
        Get items from specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`ListsResponse`: List Response
        """
        url = self.LISTS_URL + f"/users/xuid({xuid})/lists/PINS/{listname}"
        resp = await self.client.session.get(url, headers=self.HEADERS_LISTS)
        resp.raise_for_status()
        return ListsResponse.parse_raw(await resp.text())

    async def insert_items(
        self, xuid: str, post_body: dict, listname: str = "XBLPins"
    ) -> ListMetadata:
        """
        Insert items to specific list, defaults to "XBLPins"

        Args:
            xuid (str/int): Xbox User Id
            listname (str): Name of list to edit

        Returns:
            :class:`ListMetadata`: List Metadata Response
        """
        url = self.LISTS_URL + f"/users/xuid({xuid})/lists/PINS/{listname}"
        resp = await self.client.session.post(
            url, json=post_body, headers=self.HEADERS_LISTS
        )
        resp.raise_for_status()
        return ListMetadata.parse_raw(await resp.text())
