from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Menu, Restaurant
from app.schemas import MenuCreate, MenuResponse
from app.dependencies import get_db, require_restaurant

router = APIRouter(prefix="/menus", tags=["Menus"])

# ADD menu item
@router.post("/", response_model=MenuResponse)
def add_menu(
    data: MenuCreate,
    db: Session = Depends(get_db),
    user=Depends(require_restaurant)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    menu = Menu(
        restaurant_id=data.restaurant_id,
        item_name=data.item_name,
        price=data.price
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


# VIEW menu by restaurant
@router.get("/{restaurant_id}", response_model=list[MenuResponse])
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(Menu).filter(Menu.restaurant_id == restaurant_id).all()
