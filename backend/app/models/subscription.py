from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    plan_id: Mapped[str] = mapped_column(String(50))
    plan_name: Mapped[str] = mapped_column(String(100))
    plan_duration: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column(Float)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="inactive")
    payment_status: Mapped[str] = mapped_column(String(20), default="pending")

    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")
