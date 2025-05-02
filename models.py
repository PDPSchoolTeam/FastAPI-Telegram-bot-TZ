from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    verification_code = Column(String(6), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
