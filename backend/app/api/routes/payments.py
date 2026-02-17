from datetime import datetime, timedelta

import razorpay
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.payment import CreateOrderRequest, VerifyPaymentRequest

router = APIRouter(prefix="/payments", tags=["Payments"])

client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret)) if settings.razorpay_key_id else None


@router.post("/create-order")
def create_order(payload: CreateOrderRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = db.get(Subscription, payload.subscription_id)
    if not subscription or subscription.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Subscription not found")
    if subscription.payment_status == "paid":
        raise HTTPException(status_code=409, detail="Subscription already paid")

    order_data = {
        "amount": int(subscription.price * 100),
        "currency": "INR",
        "receipt": f"sub_{subscription.id}_{int(datetime.utcnow().timestamp())}",
    }
    if client:
        order = client.order.create(data=order_data)
        order_id = order["id"]
    else:
        order_id = f"mock_order_{subscription.id}_{int(datetime.utcnow().timestamp())}"

    existing = db.query(Payment).filter(Payment.order_id == order_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Duplicate order")

    payment = Payment(
        user_id=current_user.id,
        subscription_id=subscription.id,
        payment_gateway_id="pending",
        order_id=order_id,
        amount=subscription.price,
        status="created",
    )
    db.add(payment)
    db.commit()

    return {"order_id": order_id, "amount": subscription.price, "currency": "INR", "key": settings.razorpay_key_id}


@router.post("/verify")
def verify_payment(payload: VerifyPaymentRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = db.get(Subscription, payload.subscription_id)
    if not subscription or subscription.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Subscription not found")

    payment = db.query(Payment).filter(Payment.order_id == payload.razorpay_order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment order not found")
    if payment.status == "paid":
        return {"message": "Payment already verified", "subscription_status": subscription.status}

    verify_payload = {
        "razorpay_order_id": payload.razorpay_order_id,
        "razorpay_payment_id": payload.razorpay_payment_id,
        "razorpay_signature": payload.razorpay_signature,
    }

    if client:
        try:
            client.utility.verify_payment_signature(verify_payload)
        except Exception as exc:
            payment.status = "failed"
            db.commit()
            raise HTTPException(status_code=400, detail="Invalid payment signature") from exc

    payment.payment_gateway_id = payload.razorpay_payment_id
    payment.status = "paid"
    subscription.payment_status = "paid"
    subscription.status = "active"
    subscription.start_date = datetime.utcnow()
    subscription.end_date = subscription.start_date + timedelta(days=subscription.plan_duration)
    db.commit()

    return {"message": "Payment verified and subscription activated"}


@router.get("/history")
def payment_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Payment).filter(Payment.user_id == current_user.id).order_by(Payment.created_at.desc()).all()
