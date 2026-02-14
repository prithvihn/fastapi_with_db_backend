from sqlalchemy.orm import Session
from models import Conversation, Message
from datetime import datetime


class ConversationRepo:
    def __init__(self, db: Session):
        self.db = db

    # ── Conversation CRUD ─────────────────────────────────────

    def create_conversation(self, user_id: int, title: str = "New Chat") -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: int) -> Conversation | None:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_user_conversations(self, user_id: int) -> list:
        """Return all conversations for a user, most recent first, with last message preview."""
        conversations = (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

        result = []
        for conv in conversations:
            # Get the last message for preview
            last_msg = (
                self.db.query(Message)
                .filter(Message.conversation_id == conv.id)
                .order_by(Message.created_at.desc())
                .first()
            )
            result.append({
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at,
                "last_message_preview": last_msg.content[:100] if last_msg else None,
            })
        return result

    def delete_conversation(self, conversation_id: int) -> None:
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            self.db.delete(conversation)
            self.db.commit()

    def rename_conversation(self, conversation_id: int, title: str) -> Conversation | None:
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.title = title
            self.db.commit()
            self.db.refresh(conversation)
        return conversation

    def update_timestamp(self, conversation_id: int) -> None:
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.db.commit()

    # ── Message CRUD ──────────────────────────────────────────

    def add_message(self, conversation_id: int, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages(self, conversation_id: int) -> list[Message]:
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
