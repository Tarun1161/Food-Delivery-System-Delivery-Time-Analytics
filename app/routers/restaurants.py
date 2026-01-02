from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Restaurant
from app.schemas import RestaurantCreate, RestaurantResponse
from app.dependencies import get_db, require_restaurant

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


# ---------------- CREATE RESTAURANT (RESTAURANT ROLE ONLY) ----------------
@router.post("/", response_model=RestaurantResponse)
def create_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_restaurant)
):
    restaurant = Restaurant(
        name=data.name,
        location=data.location
    )

    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    return restaurant


# ---------------- LIST RESTAURANTS (PUBLIC) ----------------
@router.get("/", response_model=list[RestaurantResponse])
def list_restaurants(
    db: Session = Depends(get_db)
):
    return db.query(Restaurant).all()
