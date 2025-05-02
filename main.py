from fastapi import FastAPI
from db import engine, SessionLocal
from models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from verification_servic import generate_verification_code, verify_code
from schemas import VerificationRequest, VerificationResponse, CreateUserRequest

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/generate-code")
def generate_code(request: CreateUserRequest, db: Session = Depends(get_db)):
    code = generate_verification_code(db, request.telegram_id, request.phone_number)
    return {"verification_code": code}


@app.post("/verify", response_model=VerificationResponse)
def verify_user(request: VerificationRequest, db: Session = Depends(get_db)):
    result = verify_code(db, request.verification_code)
    return result
