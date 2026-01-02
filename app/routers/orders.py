from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Order, OrderItem, Menu
from app.schemas import OrderCreate, OrderResponse
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])
@router.post("/", response_model=OrderResponse)
def place_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # Create order
    order = Order(
        user_id=user.id,
        restaurant_id=data.restaurant_id,
        status="PLACED"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Add order items
    for item in data.items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail="Menu item not found")

        order_item = OrderItem(
            order_id=order.id,
            menu_id=item.menu_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    return order
@router.get("/my-orders", response_model=list[OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == user.id).all()
