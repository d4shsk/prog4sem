from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    rate = Column(Float, nullable=True)

    subscriptions = relationship("Subscription", back_populates="currency", cascade="all, delete-orphan")

class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    currency_id = Column(Integer, ForeignKey("currencies.id"), primary_key=True)

    user = relationship("User", back_populates="subscriptions")
    currency = relationship("Currency", back_populates="subscriptions")
