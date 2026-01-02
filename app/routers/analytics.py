from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text, extract

from app.dependencies import get_db
from app.models import Delivery, Order, Restaurant

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/avg-delivery-time")
def average_delivery_time(db: Session = Depends(get_db)):
    avg_time = db.query(
        func.avg(
            func.timestampdiff(
                text("MINUTE"),
                Delivery.assigned_at,
                Delivery.delivered_at
            )
        )
    ).filter(
        Delivery.delivered_at.isnot(None)
    ).scalar()

    return {
        "average_delivery_time_minutes": round(avg_time, 2) if avg_time else 0
    }


@router.get("/peak-hour/daily")
def daily_peak_hour(db: Session = Depends(get_db)):
    try:
        data = (
            db.query(
                extract("hour", Order.created_at).label("hour"),
                func.count(Order.id).label("orders")
            )
            .group_by("hour")
            .all()
        )

        return [
            {"hour": int(hour), "orders": orders}
            for hour, orders in data
        ]
    except Exception as e:
        return {"error": str(e)}

@router.get("/top-restaurants")
def top_restaurants(db: Session = Depends(get_db)):
    results = (
        db.query(
            Restaurant.name.label("restaurant"),
            func.count(Order.id).label("orders")
        )
        .join(Order, Order.restaurant_id == Restaurant.id)
        .group_by(Restaurant.name)
        .order_by(func.count(Order.id).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "restaurant": r.restaurant,
            "orders": int(r.orders)   # 🔥 FORCE INT
        }
        for r in results
        if r.orders > 0             # 🔥 FILTER ZERO VALUES
    ]

