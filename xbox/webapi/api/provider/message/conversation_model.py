from datetime import datetime
from typing import Any, List, Optional

from xbox.webapi.common.models import CamelCaseModel


class Part(CamelCaseModel):
    content_type: str
    text: str
    version: int
    unsuitable_for: Optional[List]


class Content(CamelCaseModel):
    parts: List[Part]


class ContentPayload(CamelCaseModel):
    content: Content


class Message(CamelCaseModel):
    content_payload: ContentPayload
    timestamp: str
    last_update_timestamp: datetime
    type: str
    network_id: str
    conversation_type: str
    conversation_id: str
    sender: str
    message_id: str
    is_deleted: bool
    is_server_updated: bool


class ConversationResponse(CamelCaseModel):
    timestamp: datetime
    network_id: str
    type: str
    conversation_id: str
    participants: List[str]
    read_horizon: str
    delete_horizon: str
    is_read: bool
    muted: bool
    folder: str
    messages: List[Message]
    continuation_token: str
    voice_id: str
    voice_roster: List[Any]
