"""
Message - Read and send messages

TODO: Support group messaging
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.message.models import (
    ConversationResponse,
    InboxResponse,
    SendMessageResponse,
)


class MessageProvider(BaseProvider):
    MSG_URL = "https://xblmessaging.xboxlive.com"
    HEADERS_MESSAGE = {"x-xbl-contract-version": "1"}
    HEADERS_HORIZON = {"x-xbl-contract-version": "2"}

    async def get_inbox(self) -> InboxResponse:
        """
        Get messages

        Args:
            skip_items: Item count to skip
            max_items: Maximum item count to load

        Returns:
            :class:`InboxResponse`: Inbox Response
        """
        url = f"{self.MSG_URL}/network/Xbox/users/me/inbox"
        resp = await self.client.session.get(url, headers=self.HEADERS_MESSAGE)
        resp.raise_for_status()
        return InboxResponse.parse_raw(await resp.text())

    async def get_conversation(
        self, xuid: str, max_items: int = 100
    ) -> ConversationResponse:
        """
        Get detailed conversation info

        Args:
            xuid: Xuid of user having a conversation with

        Returns:
            :class:`ConversationResponse`: Conversation Response
        """
        url = f"{self.MSG_URL}/network/Xbox/users/me/conversations/users/xuid({xuid})"
        params = {"maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_MESSAGE
        )
        resp.raise_for_status()
        return ConversationResponse.parse_raw(await resp.text())

    async def delete_conversation(self, conversation_id: str, horizon: str) -> bool:
        """
        Delete message

        **NOTE**: Returns HTTP Status Code **200** on success

        Args:
            conversation_id: Message Id
            horizon: Delete horizon from get conversation response

        Returns: True on success, False otherwise
        """
        url = f"{self.MSG_URL}/network/Xbox/users/me/conversations/horizon"
        post_data = {
            "conversations": [
                {
                    "conversationId": conversation_id,
                    "conversationType": "OneToOne",
                    "horizonType": "Delete",
                    "horizon": horizon,
                }
            ]
        }
        resp = await self.client.session.put(
            url, json=post_data, headers=self.HEADERS_HORIZON
        )
        return resp.status == 200

    async def delete_message(self, conversation_id: str, message_id: str) -> bool:
        """
        Delete message

        **NOTE**: Returns HTTP Status Code **200** on success

        Args:
            conversation_id: Conversation Id
            message_id: Message Id

        Returns: True on success, False otherwise
        """
        url = f"{self.MSG_URL}/network/Xbox/users/me/conversations/{conversation_id}/messages/{message_id}"
        resp = await self.client.session.delete(url, headers=self.HEADERS_MESSAGE)
        return resp.status == 200

    async def send_message(self, xuid: str, message_text: str) -> SendMessageResponse:
        """
        Send message to an xuid

        Args:
            xuid: Xuid
            message_text: Message text

        Returns:
            :class:`SendMessageResponse`: Send Message Response
        """
        if len(message_text) > 256:
            raise ValueError("Message text exceeds max length of 256 chars")

        url = f"{self.MSG_URL}/network/Xbox/users/me/conversations/users/xuid({xuid})"
        post_data = {
            "parts": [
                {
                    "contentType": "text",
                    "version": 0,
                    "text": message_text,
                }
            ]
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_MESSAGE
        )
        resp.raise_for_status()
        return SendMessageResponse.parse_raw(await resp.text())
