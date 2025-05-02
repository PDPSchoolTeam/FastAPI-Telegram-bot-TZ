from sqlalchemy.orm import Session
from models import User
from datetime import datetime,timedelta
from fastapi import HTTPException, status
import random


def verify_code(db: Session, verification_code: str):
    user = db.query(User).filter(User.verification_code == verification_code).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already verified")

    if user.verification_code != verification_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code")

    if user.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification code expired")

    user.is_verified = True
    user.verification_code = None
    user.expires_at = None
    db.commit()

    return {"message": "User verified successfully"}


def generate_verification_code(db: Session, telegram_id: int, phone_number: str):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    # Agar foydalanuvchi mavjud bo'lmasa, yangi foydalanuvchi yaratamiz # noqa
    if not user:
        user = User(
            telegram_id=telegram_id,
            phone_number=phone_number,
            is_verified=False
        )
        db.add(user)
        db.flush()  # Foydalanuvchi yaratildi, ammo commit qilinmayapti # noqa

    # Yangi verification_code generatsiya qilamiz (6 xonali raqam) # noqa
    verification_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=1)  # Kodning amal qilish muddati (1 daqiqa) # noqa

    # Yaratilgan kod va boshqa ma'lumotlarni foydalanuvchiga qo'shamiz # noqa
    user.verification_code = verification_code
    user.expires_at = expires_at
    user.is_verified = False  # Foydalanuvchi hali tasdiqlanmagan # noqa

    # Ma'lumotlarni saqlaymiz # noqa
    db.commit()
    db.refresh(user)  # Yangi foydalanuvchini yangilaymiz # noqa

    return verification_code  # Kodni qaytarish # noqa
