from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
def get_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.patch("/users/{user_id}/toggle")
def toggle_user(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user:
        user.is_active = not user.is_active
        db.commit()
    return user


@router.get("/payments")
def get_payments(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(Payment).order_by(Payment.created_at.desc()).all()


@router.get("/subscriptions")
def get_subscriptions(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(Subscription).order_by(Subscription.id.desc()).all()


@router.get("/analytics")
def analytics(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    start_day = datetime(now.year, now.month, now.day)
    start_month = datetime(now.year, now.month, 1)

    total_revenue = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.status == "paid").scalar()
    daily_revenue = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.status == "paid", Payment.created_at >= start_day)
        .scalar()
    )
    monthly_revenue = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.status == "paid", Payment.created_at >= start_month)
        .scalar()
    )

    return {
        "total_users": db.query(func.count(User.id)).scalar(),
        "active_subscriptions": db.query(func.count(Subscription.id)).filter(Subscription.status == "active").scalar(),
        "total_revenue": float(total_revenue),
        "daily_revenue": float(daily_revenue),
        "monthly_revenue": float(monthly_revenue),
    }
