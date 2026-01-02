from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str   # user / restaurant / delivery / admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RestaurantCreate(BaseModel):
    name: str
    location: str

class RestaurantResponse(RestaurantCreate):
    id: int
    rating: float

    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
    restaurant_id: int
    item_name: str
    price: float

class MenuResponse(MenuCreate):
    id: int

    class Config:
        from_attributes = True

class CartItem(BaseModel):
    menu_id: int
    quantity: int

class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[CartItem]

class OrderResponse(BaseModel):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class DeliveryAssignResponse(BaseModel):
    order_id: int
    delivery_partner_id: int
    assigned_at: datetime

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    order_id: int
    rating: int
    feedback: str | None = None

class RatingResponse(BaseModel):
    id: int
    order_id: int
    rating: int
    feedback: str | None

    class Config:
        from_attributes = True
