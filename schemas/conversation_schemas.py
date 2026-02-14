from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Conversation Schemas ──────────────────────────────────────

class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationRename(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationListItem(BaseModel):
    id: int
    title: str
    created_at: datetime
    last_message_preview: Optional[str] = None

    class Config:
        from_attributes = True


# ── Message Schemas ───────────────────────────────────────────

class MessageCreate(BaseModel):
    conversation_id: int
    content: str


class AssistantMessageCreate(BaseModel):
    conversation_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationWithMessages(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]
