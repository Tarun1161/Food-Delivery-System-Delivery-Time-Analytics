from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import DeliveryAssignResponse
from app.models import Order, Delivery, DeliveryPartner
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/delivery", tags=["Delivery"])
@router.post("/assign", response_model=DeliveryAssignResponse)
def assign_delivery_partner(
    order_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # Find order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Find available delivery partner
    partner = db.query(DeliveryPartner).filter(
        DeliveryPartner.is_available == 1
    ).first()

    if not partner:
        raise HTTPException(status_code=400, detail="No delivery partners available")

    # Assign delivery
    delivery = Delivery(
        order_id=order.id,
        delivery_partner_id=partner.id,
        assigned_at=datetime.utcnow()
    )

    order.status = "OUT_FOR_DELIVERY"
    partner.is_available = 0

    db.add(delivery)
    db.commit()

    return {
        "order_id": order.id,
        "delivery_partner_id": partner.id,
        "assigned_at": delivery.assigned_at
    }
@router.post("/delivered")
def mark_delivered(
    order_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    delivery.delivered_at = datetime.utcnow()

    order = db.query(Order).filter(Order.id == order_id).first()
    order.status = "DELIVERED"

    partner = db.query(DeliveryPartner).filter(
        DeliveryPartner.id == delivery.delivery_partner_id
    ).first()
    partner.is_available = 1

    db.commit()

    return {"message": "Order delivered successfully"}
