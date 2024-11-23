from fastapi import FastAPI
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router  # Ensure this is a FastAPI router

# Create FastAPI instance
app = FastAPI()

# Register routers
app.include_router(auth_router)
app.include_router(user_router)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
