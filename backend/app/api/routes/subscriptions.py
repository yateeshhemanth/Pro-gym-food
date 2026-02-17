from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut
from app.services.plans import PLANS

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("", response_model=list[SubscriptionOut])
def list_subscriptions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    subscriptions = db.query(Subscription).filter(Subscription.user_id == current_user.id).all()
    for sub in subscriptions:
        if sub.end_date and sub.end_date < now and sub.status == "active":
            sub.status = "expired"
    db.commit()
    return subscriptions


@router.post("/create", response_model=SubscriptionOut)
def create_subscription(payload: SubscriptionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = PLANS.get(payload.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    subscription = Subscription(
        user_id=current_user.id,
        plan_id=plan["plan_id"],
        plan_name=plan["name"],
        plan_duration=plan["duration"],
        price=plan["price"],
        status="inactive",
        payment_status="pending",
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@router.post("/{subscription_id}/cancel")
def cancel_subscription(subscription_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = db.get(Subscription, subscription_id)
    if not subscription or subscription.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = "cancelled"
    if subscription.end_date is None:
        subscription.end_date = datetime.utcnow()
    db.commit()
    return {"message": "Subscription cancelled"}
