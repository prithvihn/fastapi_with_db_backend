from fastapi import APIRouter, HTTPException
from utils.email_sender import send_email
from schemas.email_schema import EmailRequest, EmailResponse
router = APIRouter()
@router.post("/send-email", response_model=EmailResponse)
def send_email_endpoint(request: EmailRequest):
    """Send an email using the provided details."""
    try:
        result = send_email(request.recipient, request.subject, request.body)
        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail=result["message"])
        return EmailResponse(status="success", message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))