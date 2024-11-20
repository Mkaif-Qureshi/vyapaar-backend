from fastapi import FastAPI
from app.auth.auth_routes import router as auth_router

# Import other routers

app = FastAPI()

# Register routers
app.include_router(auth_router)
# Add other routers
