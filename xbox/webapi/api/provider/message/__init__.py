"""
Message - Read and send messages
"""
from typing import List

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.message.models import (
    MessageInboxResponse,
    MessageResponse,
)


class MessageProvider(BaseProvider):
    MSG_URL = "https://msg.xboxlive.com"
    HEADERS_MESSAGE = {"x-xbl-contract-version": "1"}

    async def get_message_inbox(
        self, skip_items: int = 0, max_items: int = 100
    ) -> MessageInboxResponse:
        """
        Get messages

        Args:
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns: HTTP Response
        """
        url = self.MSG_URL + f"/users/xuid({self.client.xuid})/inbox"
        params = {"skipItems": skip_items, "maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_MESSAGE
        )
        resp.raise_for_status()
        return MessageInboxResponse.parse_raw(await resp.text())

    async def get_message(self, message_id: str) -> MessageResponse:
        """
        Get detailed message info

        Args:
            message_id: Message Id

        Returns: HTTP Response
        """
        url = self.MSG_URL + f"/users/xuid({self.client.xuid})/inbox/{message_id}"
        resp = await self.client.session.get(url, headers=self.HEADERS_MESSAGE)
        resp.raise_for_status()
        return MessageResponse.parse_raw(await resp.text())

    async def delete_message(self, message_id: str) -> bool:
        """
        Delete message

        **NOTE**: Returns HTTP Status Code **204** on success

        Args:
            message_id: Message Id

        Returns: True on success, False otherwise
        """
        url = self.MSG_URL + f"/users/xuid({self.client.xuid})/inbox/{message_id}"
        resp = await self.client.session.delete(url, headers=self.HEADERS_MESSAGE)
        return resp.status == 204

    async def send_message(
        self, message_text: str, gamertags: List[str] = None, xuids: List[str] = None
    ):
        """
        Send message to a list of gamertags

        Only one of each recipient types can be supplied,
        either gamertags **or** xuids

        Args:
            message_text: Message text
            gamertags (list): List of recipients by gamertag
            xuids: List of recipiencts by xuid

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        if len(message_text) > 256:
            raise ValueError("Message text exceeds max length of 256 chars")

        if gamertags and xuids:
            raise ValueError("Either pass gamertags or xuids, not both!")
        elif gamertags:
            recipients = [dict(gamertag=gtg) for gtg in gamertags]
        elif xuids:
            recipients = [dict(xuid=xid) for xid in xuids]
        else:
            raise ValueError("No recipients are passed")

        url = self.MSG_URL + f"/users/xuid({self.client.xuid})/outbox"
        post_data = {"header": {"recipients": recipients}, "messageText": message_text}
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_MESSAGE
        )
        return resp.status == 200
