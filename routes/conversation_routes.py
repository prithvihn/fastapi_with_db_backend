from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db import get_db
from utils.auth import get_current_user
from repositories.conversation_repo import ConversationRepo
from schemas.conversation_schemas import (
    ConversationCreate,
    ConversationResponse,
    ConversationListItem,
    ConversationRename,
    MessageCreate,
    MessageResponse,
    AssistantMessageCreate,
)

router = APIRouter(prefix="/api", tags=["Conversations & Messages"])


# ── Helper ────────────────────────────────────────────────────

def _verify_ownership(repo: ConversationRepo, conversation_id: int, user_id: int):
    """Return the conversation if it exists and belongs to the user, else raise."""
    conversation = repo.get_conversation_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    if conversation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this conversation")
    return conversation


# ── Conversation Endpoints ────────────────────────────────────

@router.post("/conversations/create", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    body: ConversationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Create a new conversation for the logged-in user."""
    repo = ConversationRepo(db)
    title = body.title if body.title else "New Chat"
    # Auto-trim title to 50 characters
    title = title[:50]
    conversation = repo.create_conversation(user_id=user_id, title=title)
    return conversation


@router.get("/conversations/list", response_model=list[ConversationListItem])
def list_conversations(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Get all conversations for the logged-in user, most recent first."""
    repo = ConversationRepo(db)
    return repo.get_user_conversations(user_id)


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Get all messages in a conversation. Verifies ownership."""
    repo = ConversationRepo(db)
    _verify_ownership(repo, conversation_id, user_id)
    return repo.get_messages(conversation_id)


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Delete a conversation and all its messages. Verifies ownership."""
    repo = ConversationRepo(db)
    _verify_ownership(repo, conversation_id, user_id)
    repo.delete_conversation(conversation_id)
    return None


@router.patch("/conversations/{conversation_id}/rename", response_model=ConversationResponse)
def rename_conversation(
    conversation_id: int,
    body: ConversationRename,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Rename a conversation. Verifies ownership."""
    repo = ConversationRepo(db)
    _verify_ownership(repo, conversation_id, user_id)
    conversation = repo.rename_conversation(conversation_id, body.title[:50])
    return conversation


# ── Message Endpoints ─────────────────────────────────────────

@router.post("/messages/create", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_user_message(
    body: MessageCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Save a user message to a conversation. Verifies ownership."""
    repo = ConversationRepo(db)
    conversation = _verify_ownership(repo, body.conversation_id, user_id)

    message = repo.add_message(conversation_id=body.conversation_id, role="user", content=body.content)

    # Auto-generate title from first user message (first 50 chars)
    if conversation.title == "New Chat":
        repo.rename_conversation(conversation.id, body.content[:50])

    repo.update_timestamp(body.conversation_id)
    return message


@router.post("/messages/save-assistant", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def save_assistant_message(
    body: AssistantMessageCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """Save an assistant response to a conversation. Verifies ownership and updates timestamp."""
    repo = ConversationRepo(db)
    _verify_ownership(repo, body.conversation_id, user_id)

    message = repo.add_message(conversation_id=body.conversation_id, role="assistant", content=body.content)
    repo.update_timestamp(body.conversation_id)
    return message
