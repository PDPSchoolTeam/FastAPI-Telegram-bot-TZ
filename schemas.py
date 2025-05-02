from pydantic import BaseModel, Field


class VerificationRequest(BaseModel):
    verification_code: str = Field(..., min_length=6, max_length=6)  # faqat 6 ta raqam


class VerificationResponse(BaseModel):
    message: str


class CreateUserRequest(BaseModel):
    telegram_id: int
    phone_number: str
