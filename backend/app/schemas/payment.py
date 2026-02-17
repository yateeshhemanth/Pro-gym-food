from datetime import datetime

from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    subscription_id: int


class VerifyPaymentRequest(BaseModel):
    subscription_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentOut(BaseModel):
    id: int
    payment_gateway_id: str
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
