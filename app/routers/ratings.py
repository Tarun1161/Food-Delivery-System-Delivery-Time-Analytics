from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Rating, Order, Restaurant
from app.schemas import RatingCreate, RatingResponse
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", response_model=RatingResponse)
def add_rating(
    data: RatingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 1. Check order exists
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. Only delivered orders can be rated
    if order.status != "DELIVERED":
        raise HTTPException(
            status_code=400,
            detail="You can rate only delivered orders"
        )

    # 3. Prevent duplicate rating
    existing = db.query(Rating).filter(
        Rating.order_id == data.order_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Order already rated"
        )

    # 4. Save rating
    rating = Rating(
        order_id=data.order_id,
        rating=data.rating,
        feedback=data.feedback
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)

    # 5. Update restaurant average rating (SAFE)
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == order.restaurant_id
    ).first()

    avg_rating = db.query(func.avg(Rating.rating)).join(Order).filter(
        Order.restaurant_id == restaurant.id
    ).scalar()

    restaurant.rating = round(avg_rating, 1)
    db.commit()

    return rating


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[RatingResponse]
)
def get_restaurant_ratings(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    ratings = db.query(Rating).join(Order).filter(
        Order.restaurant_id == restaurant_id
    ).all()

    return ratings


