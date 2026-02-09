from fastapi import APIRouter, HTTPException
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse

router = APIRouter()


@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest):
    """Get response from AI model."""
    try:
        response = get_completion(request.message, request.system_prompt)
        return AIResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 