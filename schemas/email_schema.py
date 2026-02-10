from pydantic import BaseModel, EmailStr
class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
class EmailResponse(BaseModel):
    status: str
    message: str