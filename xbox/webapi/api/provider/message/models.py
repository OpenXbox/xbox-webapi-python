from datetime import datetime
from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel


class Part(CamelCaseModel):
    content_type: str
    version: int
    text: str
    unsuitable_for: Optional[List]
    locator: Optional[str]


class Content(CamelCaseModel):
    parts: List[Part]


class ContentPayload(CamelCaseModel):
    content: Content


class Message(CamelCaseModel):
    content_payload: Optional[ContentPayload]
    timestamp: datetime
    last_update_timestamp: datetime
    type: str
    network_id: str
    conversation_type: str
    conversation_id: str
    owner: Optional[int]
    sender: str
    message_id: str
    is_deleted: bool
    is_server_updated: bool


class Conversation(CamelCaseModel):
    timestamp: datetime
    network_id: str
    type: str
    conversation_id: str
    voice_id: str
    participants: List[str]
    read_horizon: str
    delete_horizon: str
    is_read: bool
    muted: bool
    folder: str
    last_message: Message


class Primary(CamelCaseModel):
    folder: str
    total_count: int
    unread_count: int
    conversations: List[Conversation]


class SafetySettings(CamelCaseModel):
    version: int
    primary_inbox_media: str
    primary_inbox_text: str
    primary_inbox_url: str
    secondary_inbox_media: str
    secondary_inbox_text: str
    secondary_inbox_url: str
    can_unobscure: bool


class InboxResponse(CamelCaseModel):
    primary: Primary
    folders: List[Any]
    safety_settings: SafetySettings


class ConversationResponse(CamelCaseModel):
    timestamp: datetime
    network_id: str
    type: str
    conversation_id: str
    participants: Optional[List[str]]
    read_horizon: str
    delete_horizon: str
    is_read: bool
    muted: bool
    folder: str
    messages: Optional[List[Message]]
    continuation_token: Optional[str]
    voice_id: str
    voice_roster: Optional[List[Any]]


class SendMessageResponse(CamelCaseModel):
    message_id: str
    conversation_id: str
