from datetime import datetime

from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    plan_id: str


class SubscriptionOut(BaseModel):
    id: int
    plan_id: str
    plan_name: str
    plan_duration: int
    price: float
    start_date: datetime | None
    end_date: datetime | None
    status: str
    payment_status: str

    class Config:
        from_attributes = True
