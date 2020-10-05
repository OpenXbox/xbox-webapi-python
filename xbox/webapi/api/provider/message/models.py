from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel


class MessageHeader(CamelCaseModel):
    id: Optional[str]
    is_read: Optional[bool]
    sender_xuid: int
    sender: str
    sent: str
    expiration: str
    message_type: str
    has_text: bool
    has_photo: bool
    has_audio: bool
    message_folder_type: str


class MessageResponse(CamelCaseModel):
    header: MessageHeader
    messageText: str
    attachmentId: Any
    attachment: Any


class InboxResult(CamelCaseModel):
    header: MessageHeader
    message_summary: str


class PagingInfo(CamelCaseModel):
    continuation_token: Any
    total_items: int


class MessageInboxResponse(CamelCaseModel):
    results: List[InboxResult]
    paging_info: PagingInfo
