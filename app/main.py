from fastapi import FastAPI
from fastapi.responses import JSONResponse

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app.database import engine
from app import models
from app.core.limiter import limiter
from app.routers import (
    auth,
    restaurants,
    menus,
    orders,
    delivery,
    ratings,
    analytics
)

app = FastAPI(title="Food Delivery System")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Create DB tables AFTER app startup
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

# Attach limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Rate limit error handler
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, please try again later"}
    )

# Root endpoint
@app.get("/")
def root():
    return {"message": "Food Delivery API is running"}

# Routers
app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(menus.router)
app.include_router(orders.router)
app.include_router(delivery.router)
app.include_router(ratings.router)
app.include_router(analytics.router)
